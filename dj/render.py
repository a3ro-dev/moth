"""The hands: turns a mix plan into audio. Pure, deterministic DSP, no AI here.

Plan shape (what the brain writes):
{
  "tracks": [{"id": "...", "cue_in_bar": 0, "play_bpm": 120.0?}, ...],
  "transitions": [{"start_bar": 96, "bars": 16, "type": "bass_swap", "why": "..."}, ...]
}
transitions[i] goes from tracks[i] to tracks[i+1]. start_bar is in the outgoing track's bars;
the incoming track's cue_in_bar lands exactly on it.

Each deck carries a time map (source seconds -> mix seconds). During a beatmatched overlap the
incoming deck is warped bar by bar so every one of its downbeats lands on the outgoing deck's
downbeat, which keeps drifting (live / desi) grids locked instead of trainwrecking.
"""
import json
import subprocess
from pathlib import Path

import numpy as np
from scipy.signal import butter, sosfiltfilt

from analyze import CACHE, band_energy, waveform

SR = 44100
OUT = Path(__file__).resolve().parent.parent / "data" / "mixes"
TARGET_LUFS = -10.0
BEATMATCHED = {"blend", "bass_swap", "eq_swap", "filter"}
TYPES = BEATMATCHED | {"echo_out", "cut"}
XF = int(0.006 * SR)  # crossfade between warped segments
PAD = 0.15  # seconds of context around each stretched segment

LOW = butter(4, 200, "lowpass", fs=SR, output="sos")
HIGH = butter(4, 2500, "highpass", fs=SR, output="sos")


def decode(path: str) -> np.ndarray:
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-ac", "2", "-ar", str(SR), "-f", "f32le", "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, dtype=np.float32).reshape(-1, 2).copy()


def master(mix: np.ndarray, lufs=-10.0, ceiling=0.89) -> np.ndarray:
    """Loudness-normalize, then a 5 ms look-ahead brickwall limiter (no clipping distortion)."""
    from scipy.ndimage import maximum_filter1d, uniform_filter1d
    import pyloudnorm
    loud = pyloudnorm.Meter(SR).integrated_loudness(mix.astype(np.float64))
    if np.isfinite(loud):
        mix = mix * 10 ** ((lufs - loud) / 20)
    la = int(0.005 * SR)
    need = np.minimum(1, ceiling / np.maximum(np.abs(mix).max(axis=1), 1e-9))
    g = -maximum_filter1d(-need, 2 * la + 1)  # hold the gain dip across the look-ahead window
    g = uniform_filter1d(g, la)  # smooth the attack/release so it doesn't buzz
    g = np.minimum(g, need)  # never let smoothing overshoot the ceiling
    return (mix * g[:, None]).astype(np.float32)


def stretch(x: np.ndarray, ratio: float, semitones: float = 0) -> np.ndarray:
    """Rubberband time-stretch (pitch preserved) and optional pitch shift. ratio > 1 = faster/shorter."""
    if abs(ratio - 1) < 1e-4 and not semitones:
        return x
    out = subprocess.run(["ffmpeg", "-v", "error", "-f", "f32le", "-ar", str(SR), "-ac", "2", "-i", "-",
                          "-af", f"rubberband=tempo={ratio:.6f}:pitch={2 ** (semitones / 12):.6f}:transients=crisp:pitchq=quality",
                          "-f", "f32le", "-"], input=x.astype(np.float32).tobytes(), capture_output=True, check=True).stdout
    return np.frombuffer(out, dtype=np.float32).reshape(-1, 2).copy()


class Deck:
    def __init__(self, meta, audio):
        self.meta, self.audio = meta, audio
        self.db = np.array(meta["downbeats"])
        self.S, self.M, self.rate = [], [], 1.0  # anchors (source s, mix s); rate = source s per mix s

    def to_mix(self, src):
        src = np.atleast_1d(np.asarray(src, float))
        S, M = np.array(self.S), np.array(self.M)
        out = np.interp(src, S, M)
        out[src > S[-1]] = M[-1] + (src[src > S[-1]] - S[-1]) / self.rate
        out[src < S[0]] = M[0] - (S[0] - src[src < S[0]]) / self.rate
        return out

    def bar_mix(self, b):
        return float(self.to_mix(self.db[min(b, len(self.db) - 1)])[0])

    def render(self, src0, src1):
        """Audio for source range [src0, src1] laid out in mix time. Returns (mix_start_sample, audio)."""
        knots = [src0] + [s for s in self.S if src0 < s < src1] + [src1]
        m0 = int(round(self.to_mix(src0)[0] * SR))
        total = int(round(self.to_mix(src1)[0] * SR)) - m0
        out = np.zeros((total + XF, 2), np.float32)
        for a, b in zip(knots, knots[1:]):
            ma, mb = (self.to_mix([a, b]) * SR).round().astype(int)
            n = mb - ma
            if n <= 0:
                continue
            ratio = (b - a) * SR / n
            lo, hi = max(0, int((a - PAD) * SR)), min(len(self.audio), int((b + PAD) * SR))
            y = stretch(self.audio[lo:hi], ratio)
            skip = int(round((a * SR - lo) / ratio))
            seg = y[skip: skip + n + XF]
            if len(seg) < n + XF:
                seg = np.pad(seg, ((0, n + XF - len(seg)), (0, 0)))
            o = ma - m0
            if o > 0:  # crossfade into the previous segment's tail
                f = np.linspace(0, 1, XF, dtype=np.float32)[:, None]
                seg[:XF] = seg[:XF] * f + out[o: o + XF] * (1 - f)
            out[o: o + n + XF] = seg[: len(out) - o]
        gain = 10 ** ((TARGET_LUFS - self.meta["lufs"]) / 20)
        return m0, out[:total] * gain


def split3(x):
    lo = sosfiltfilt(LOW, x, axis=0)
    hi = sosfiltfilt(HIGH, x, axis=0)
    return lo, x - lo - hi, hi  # zero-phase split: sums back to x exactly at unity gain


def ramp(n, pts):
    """Piecewise-linear envelope over n samples; pts = [(fraction, gain), ...]."""
    xs, ys = zip(*pts)
    return np.interp(np.linspace(0, 1, n), xs, ys).astype(np.float32)


def curves(kind, n, b, sw=0.5):
    """Gain envelopes (low, mid, high) for outgoing A and incoming B over an overlap of n samples.
    b: one beat as a fraction of the overlap, so swaps snap to a beat. sw: where the bass swap lands."""
    if kind == "blend":
        a = [ramp(n, [(0, 1), (sw - b, 1), (sw, 0), (1, 0)]), ramp(n, [(0, 1), (sw, 1), (1, 0)]), ramp(n, [(0, 1), (sw, 1), (1, 0)])]
        bb = [ramp(n, [(0, 0), (sw - b, 0), (sw, 1), (1, 1)]), ramp(n, [(0, 0), (sw, 1), (1, 1)]), ramp(n, [(0, 0), (sw, 1), (1, 1)])]
        return a, bb
    if kind == "bass_swap":
        a = [ramp(n, [(0, 1), (sw - b, 1), (sw, 0), (1, 0)]), ramp(n, [(0, 1), (sw, .85), (1, 0)]), ramp(n, [(0, 1), (sw, .7), (1, 0)])]
        bb = [ramp(n, [(0, 0), (sw - b, 0), (sw, 1), (1, 1)]), ramp(n, [(0, .3), (sw, 1), (1, 1)]), ramp(n, [(0, .5), (sw, 1), (1, 1)])]
        return a, bb
    if kind == "eq_swap":  # highs in, lows swap at sw, mids swap later, A's highs leave last
        m = min(.95, sw + .25)
        a = [ramp(n, [(0, 1), (sw - b, 1), (sw, 0), (1, 0)]), ramp(n, [(0, 1), (m - b, 1), (m, 0), (1, 0)]),
             ramp(n, [(0, 1), (m, 1), (1, 0)])]
        bb = [ramp(n, [(0, 0), (sw - b, 0), (sw, 1), (1, 1)]), ramp(n, [(0, 0), (sw, .4), (m - b, .4), (m, 1), (1, 1)]),
              ramp(n, [(0, 0), (sw / 2, 1), (1, 1)])]
        return a, bb
    if kind == "filter":
        # ponytail: band-gain approximation of a high-pass sweep on A; true resonant swept filter later
        a = [ramp(n, [(0, 1), (.4, 0), (1, 0)]), ramp(n, [(0, 1), (.6, .6), (1, 0)]), ramp(n, [(0, 1), (.8, 1), (1, 0)])]
        bb = [ramp(n, [(0, 0), (1 - b, 0), (1, 1)]), ramp(n, [(0, 0), (.6, .8), (1, 1)]), ramp(n, [(0, 0), (.5, 1), (1, 1)])]
        return a, bb
    raise ValueError(kind)


def echo_tail(x, beat, length, feedback=0.55):
    """Ping-pong feedback delay (3/4 beat) fed by the last beat of A; rings out over `length` samples."""
    delay = int(beat * 0.75)
    out = np.zeros((length + len(x), 2), np.float32)
    g = 1.0
    for k in range(1, 64):
        g *= feedback
        if g < 0.01 or k * delay >= len(out):
            break
        seg = x[: len(out) - k * delay] * g
        out[k * delay: k * delay + len(seg)] += seg if k % 2 else seg[:, ::-1]
    return out[len(x):]


def load_meta(ids):
    return [json.loads((CACHE / f"{i}.json").read_text()) for i in ids]


def render(plan: dict, name: str) -> dict:
    tracks, trans = plan["tracks"], plan["transitions"]
    assert len(trans) == len(tracks) - 1, "need exactly one transition between consecutive tracks"
    meta = load_meta([t["id"] for t in tracks])
    decks = [Deck(m, decode(m["path"])) for m in meta]

    # --- time maps
    d0 = decks[0]
    d0.rate = tracks[0].get("play_bpm", meta[0]["bpm"]) / meta[0]["bpm"]
    c0 = tracks[0].get("cue_in_bar", 0)
    d0.S, d0.M = [d0.db[c0]], [0.0]
    for i, tr in enumerate(trans):
        A, B = decks[i], decks[i + 1]
        s, n, cue = tr["start_bar"], tr["bars"], tracks[i + 1].get("cue_in_bar", 0)
        if tr["type"] in BEATMATCHED:
            B.S = [B.db[cue + j] for j in range(n + 1)]
            B.M = [A.bar_mix(s + j) for j in range(n + 1)]
            k = min(4, n)  # carry the tempo of the last bars of the overlap forward
            B.rate = (B.S[-1] - B.S[-1 - k]) / (B.M[-1] - B.M[-1 - k])
        else:
            B.S, B.M = [B.db[cue]], [A.bar_mix(s)]
            B.rate = tracks[i + 1].get("play_bpm", B.meta["bpm"]) / B.meta["bpm"]
        tracks[i + 1]["play_bpm"] = round(B.meta["bpm"] * B.rate, 2)
    tracks[0]["play_bpm"] = round(meta[0]["bpm"] * d0.rate, 2)

    # --- render decks with EQ/fader automation in mix time
    parts, timeline, windows = [], [], []
    for i, d in enumerate(decks):
        cue = tracks[i].get("cue_in_bar", 0)
        src0 = d.db[cue]
        last = i == len(decks) - 1
        if last:
            src1 = len(d.audio) / SR
        elif trans[i]["type"] in BEATMATCHED:
            src1 = d.db[min(trans[i]["start_bar"] + trans[i]["bars"], len(d.db) - 1)]
        else:
            src1 = d.db[trans[i]["start_bar"]]
        m0, x = d.render(src0, src1)
        bands = list(split3(x))
        gains = [np.ones(len(x), np.float32) for _ in range(3)]

        def env(tr, deck_idx, side):
            a0 = int(round(decks[deck_idx].bar_mix(tr["start_bar"]) * SR))
            a1 = int(round(decks[deck_idx].bar_mix(tr["start_bar"] + tr["bars"]) * SR))
            ab = curves(tr["type"], a1 - a0, 0.25 / tr["bars"], tr.get("swap_at", 0.5))
            for k in range(3):
                lo, hi = a0 - m0, a1 - m0
                e = ab[side][k]
                cl, ch = max(lo, 0), min(hi, len(x))
                if ch > cl:
                    gains[k][cl:ch] *= e[cl - lo: ch - lo]

        if i > 0 and trans[i - 1]["type"] in BEATMATCHED:
            env(trans[i - 1], i - 1, 1)
        if not last and trans[i]["type"] in BEATMATCHED:
            env(trans[i], i, 0)
        y = sum(b * g[:, None] for b, g in zip(bands, gains))
        fade = min(64, len(y))
        y[:fade] *= np.linspace(0, 1, fade, dtype=np.float32)[:, None]
        y[-fade:] *= np.linspace(1, 0, fade, dtype=np.float32)[:, None]
        parts.append((m0, y))
        if not last and trans[i]["type"] == "echo_out":
            beat = int(np.median(np.diff(d.db)) / 4 / d.rate * SR)
            tail = echo_tail(x[-beat:], beat, int(max(1, trans[i]["bars"]) * 4 * beat))
            parts.append((m0 + len(x), tail * 0.8))
        timeline.append({"id": d.meta["id"], "title": d.meta["title"], "mix_start": m0 / SR, "mix_end": (m0 + len(x)) / SR,
                         "play_bpm": tracks[i]["play_bpm"], "stretch_pct": round((d.rate - 1) * 100, 2),
                         "camelot": d.meta["camelot"], "key": d.meta["key"]})

    total = max(o + len(y) for o, y in parts)
    mix = np.zeros((total, 2), np.float32)
    for o, y in parts:
        mix[o: o + len(y)] += y
    peak = float(np.abs(mix).max())
    mix = master(mix)

    for i, tr in enumerate(trans):
        A, B = decks[i], decks[i + 1]
        t0, t1 = A.bar_mix(tr["start_bar"]), A.bar_mix(tr["start_bar"] + tr["bars"])
        err = None
        if tr["type"] in BEATMATCHED:  # verifiable: B's downbeats vs A's downbeats in mix time
            cue = tracks[i + 1].get("cue_in_bar", 0)
            a = np.array([A.bar_mix(tr["start_bar"] + j) for j in range(tr["bars"] + 1)])
            b = B.to_mix(B.db[cue: cue + tr["bars"] + 1])
            err = round(float(np.abs(a[: len(b)] - b).max() * 1000), 1)
        windows.append({"index": i, "type": tr["type"], "bars": tr["bars"], "mix_start": t0, "mix_end": t1,
                        "downbeat_error_ms": err, "why": tr.get("why", "")})

    OUT.mkdir(parents=True, exist_ok=True)
    mp3 = OUT / f"{name}.mp3"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "2", "-i", "-",
                    "-b:a", "256k", str(mp3)], input=mix.tobytes(), check=True)
    for w in windows:  # preview clips for the critic: 8 bars before -> 8 bars after
        bar = float(np.median(np.diff(decks[w["index"]].db))) / decks[w["index"]].rate
        a, b = max(0, w["mix_start"] - 8 * bar), min(total / SR, w["mix_end"] + 8 * bar)
        clip = OUT / f"{name}_t{w['index']}.mp3"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{a:.3f}", "-to", f"{b:.3f}", "-i", str(mp3),
                        "-b:a", "192k", str(clip)], check=True)
        w["clip"], w["clip_offset"] = clip.name, a
    wave = waveform(band_energy(np.ascontiguousarray(mix.mean(axis=1)[::2]), 512), 2400)
    result = {"name": name, "file": mp3.name, "duration": total / SR, "peak": peak, "waveform": wave, "timeline": timeline,
              "transitions": windows, "plan": plan}
    (OUT / f"{name}.json").write_text(json.dumps(result, indent=1))
    return result


if __name__ == "__main__":
    import sys
    r = render(json.loads(Path(sys.argv[1]).read_text()), sys.argv[2] if len(sys.argv) > 2 else "test")
    print(json.dumps({k: r[k] for k in ("file", "duration", "peak", "timeline", "transitions")}, indent=1))
