"""The performance sequencer: stems + moves on a master grid. This is what makes it DJing, not stitching.

Routine (what MOTH writes):
{
  "master_bpm": 120, "decks": {"A": {"id": "...", "semitones": 0, "tempo_mult": 1}, "B": {...}},
  "events": [{"at": 0, "move": "play", "deck": "A", "stems": ["drums","bass","other"], "src": 16, "bars": 8,
              "fade_in": 0, "fade_out": 0, "filter": "lp_up", "echo": false, "gain": 1, "note": "..."}, ...]
}
All positions are bars: `at` on the master grid, `src` in the deck's own bar numbers (fractions = beats, 0.25 = 1 beat).

Moves:
  play       stems of a deck from src for `bars`
  loop       a `beats`-long slice from src repeated for `bars`
  roll       build-up: loop that halves (beats, beats/2, /4, /8) across `bars`
  chop       a `beats`-long slice from src fired at each `hits` (beat offsets from at): "gol-gol-GOLMAAL"
  riser      noise sweep over `bars`, peaking at at+bars
  impact     sub drop + hit at `at`
  gap        silence the whole mix for `beats` from at (the pull before the drop)
  tape_stop  everything slows to a halt over `beats`
  backspin   the last moments spin backwards over `beats`
"""
import json
import subprocess
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import numpy as np
from scipy.signal import butter, sosfilt

import measure
import render
from mixer import KNOBS as mixer_knobs, mixer as console_mix
import rules
import stems as stemlib
from analyze import CACHE, band_energy, waveform

SR = 44100
OUT = render.OUT
MOVES = ("play", "loop", "roll", "chop", "riser", "impact", "gap", "tape_stop", "backspin")
STEM_NAMES = ("vocals", "drums", "bass", "other")
TARGET_LUFS = -10.0


class Deck:
    def __init__(self, spec, master_bpm, window=None):
        self.meta = stemlib.profile(spec["id"])
        self.semitones = float(spec.get("semitones", 0))
        bpm = self.meta["bpm"] * float(spec.get("tempo_mult", 1))
        self.ratio = master_bpm / bpm  # playback speed
        self.db = np.array(self.meta["downbeats"])
        self.gain = 10 ** ((TARGET_LUFS - self.meta["lufs"]) / 20)
        self.raw = stemlib.stems(spec["id"])
        # only stretch the source bars the routine touches (+1 bar margin): full stems take a minute
        lo, hi = window or (0, len(self.db))
        self.t0 = float(np.interp(max(0, lo - 1), np.arange(len(self.db)), self.db))
        self.t1 = float(np.interp(min(len(self.db) - 1, hi + 1), np.arange(len(self.db)), self.db)) if hi + 1 < len(self.db) else None
        self.cache = {}
        self.window = (lo, hi)

    def prepare(self, names):
        todo = [n for n in names if n not in self.cache]
        a, b = int(self.t0 * SR), (int(self.t1 * SR) if self.t1 else None)
        with ThreadPoolExecutor(4) as ex:
            for n, y in zip(todo, ex.map(lambda n: render.stretch(np.asarray(self.raw[n][a:b]), self.ratio, self.semitones), todo)):
                self.cache[n] = y * self.gain

    def stem(self, name):
        self.prepare([name])
        return self.cache[name]

    def pos(self, src_bar):
        """Sample index in the stretched window of a (fractional) source bar."""
        t = np.interp(src_bar, np.arange(len(self.db)), self.db)
        return max(0, int(round((t - self.t0) / self.ratio * SR)))

    def slice(self, names, src_bar, n):
        a = self.pos(src_bar)
        out = np.zeros((n, 2), np.float32)
        for s in names:
            x = self.stem(s)[a: a + n]
            out[: len(x)] += x
        return out


def sweep(x, kind):
    """Time-varying 2nd-order filter, cutoff moves log-linearly across the event (block-processed)."""
    lo_hi = {"hp_up": ("highpass", 30, 3000), "hp_down": ("highpass", 3000, 30),
             "lp_down": ("lowpass", 16000, 250), "lp_up": ("lowpass", 250, 16000)}
    btype, f0, f1 = lo_hi[kind]
    out = np.empty_like(x)
    zi = np.zeros((1, 2, 2))
    block = 1024
    nb = max(1, (len(x) + block - 1) // block)
    for i in range(nb):
        fc = f0 * (f1 / f0) ** (i / max(1, nb - 1))
        sos = butter(2, min(fc, SR / 2 * 0.95), btype, fs=SR, output="sos")
        seg = x[i * block:(i + 1) * block]
        out[i * block:(i + 1) * block], zi = sosfilt(sos, seg, axis=0, zi=zi)
    return out


def env(n, fade_in, fade_out):
    e = np.ones(n, np.float32)
    if fade_in:
        k = min(n, fade_in)
        e[:k] *= np.linspace(0, 1, k) ** 2
    if fade_out:
        k = min(n, fade_out)
        e[n - k:] *= np.linspace(1, 0, k) ** 2
    return e


def declick(x, k=96):
    k = min(k, len(x) // 2)
    if k:
        x[:k] *= np.linspace(0, 1, k, dtype=np.float32)[:, None]
        x[-k:] *= np.linspace(1, 0, k, dtype=np.float32)[:, None]
    return x


def riser(n):
    t = np.linspace(0, 1, n)
    noise = np.random.default_rng(7).standard_normal((n, 2)).astype(np.float32)
    out = np.empty_like(noise)
    zi = np.zeros((1, 2, 2))
    for i in range(0, n, 1024):  # band-pass sweeping up 400 Hz -> 9 kHz
        fc = 400 * (9000 / 400) ** (i / n)
        sos = butter(1, [fc * 0.7, min(fc * 1.4, SR / 2 * 0.95)], "bandpass", fs=SR, output="sos")
        out[i:i + 1024], zi = sosfilt(sos, noise[i:i + 1024], axis=0, zi=zi)
    return out * (t ** 2.2)[:, None].astype(np.float32) * 0.35


def impact(n):
    t = np.arange(n) / SR
    sub = np.sin(2 * np.pi * (55 * t - 12 * t ** 2)) * np.exp(-t * 2.2)
    hit = np.random.default_rng(3).standard_normal(n) * np.exp(-t * 18) * 0.3
    return np.repeat(((sub * 0.6 + hit) * (t < 2.5))[:, None], 2, axis=1).astype(np.float32)


# how long a stem rings out when it leaves (in bars), high-passed and faded like pulling a fader with the low EQ cut
TAILS = {"vocals": 0.25, "drums": 0.5, "bass": 0.25, "other": 1.0}


def _joins(a, b, s):
    """Does play b continue play a's stem s seamlessly (same deck, next source bar right where a ends)?"""
    return (a is not b and a["move"] == b["move"] == "play" and a.get("deck") == b.get("deck")
            and s in (a.get("stems") or STEM_NAMES) and s in (b.get("stems") or STEM_NAMES)
            and abs(float(a["at"]) + float(a.get("bars", 1)) - float(b["at"])) < 1e-6
            and abs(float(a.get("src", 0)) + float(a.get("bars", 1)) - float(b.get("src", 0))) < 1e-6)


def _swaps(a, b, s):
    """Does play b take over stem s from a DIFFERENT deck's play a right where a ends (a beat handoff)?"""
    return (a is not b and a["move"] == b["move"] == "play" and a.get("deck") != b.get("deck")
            and s in (a.get("stems") or STEM_NAMES) and s in (b.get("stems") or STEM_NAMES)
            and abs(float(a["at"]) + float(a.get("bars", 1)) - float(b["at"])) < 1e-6)


def play_seams(e, events, d, names, src, n, S):
    """Body of a play event plus the tail of every stem that leaves. Seamless continuations get no fades at all;
    fresh entries get a 5 ms declick; leaving stems ring out (TAILS) through a rising high-pass instead of stopping dead."""
    body = np.zeros((n, 2), np.float32)
    tail = np.zeros((S(max(TAILS.values())), 2), np.float32)
    for s in names:
        cont_in = any(_joins(p, e, s) for p in events)
        cont_out = any(_joins(e, q, s) for q in events)
        # bass handoff between decks: a 1-bar equal-gain crossfade (out cos², in sin²) instead of a cut
        swap_in = s == "bass" and any(_swaps(p, e, s) for p in events) and n >= S(1)
        swap_out = s == "bass" and any(_swaps(e, q, s) for q in events)
        t = 0 if cont_out or e.get("fade_out") else S(1) if swap_out else S(TAILS[s])
        x = d.slice([s], src, n + t)
        if swap_in:
            x[:S(1)] *= (np.sin(np.linspace(0, np.pi / 2, S(1), dtype=np.float32)) ** 2)[:, None]
        elif not cont_in:
            x[:220] *= np.linspace(0, 1, 220, dtype=np.float32)[:, None]
        body += x[:n]
        if t:
            rt = x[n:].copy()
            rt = sweep(rt, "hp_up") if s != "bass" else rt
            rt *= np.cos(np.linspace(0, np.pi / 2, len(rt), dtype=np.float32))[:, None] ** 2
            tail[: len(rt)] += rt
    return body, tail


def render_move(e, events, d, names, src, n, S, beat, key, o, put):
    """One deck move for one stem group. Returns (audio, length); play tails go straight onto the bus."""
    mv = e["move"]
    if mv == "play":
        x, tail = play_seams(e, events, d, names, src, n, S)
        put(key, o + n, tail)
    elif mv == "loop":
        seg = declick(d.slice(names, src, max(64, S(e.get("beats", 4) / 4))), 48)
        x = np.tile(seg, (n // len(seg) + 1, 1))[:n]
    elif mv == "roll":
        b0 = float(e.get("beats", 1))
        parts = []
        for k in range(4):
            seg = declick(d.slice(names, src, max(64, S(b0 / 2 ** k / 4))), 32)
            q = n // 4
            parts.append(np.tile(seg, (q // len(seg) + 1, 1))[:q] * (0.75 + 0.08 * k))
        x = np.concatenate(parts)
        n = len(x)
    else:  # chop
        seg = d.slice(names, src, max(64, S(min(float(e.get("beats", 1)), 2) / 4)))
        hits = sorted(e.get("hits") or [0])
        n = int(max(hits) * beat * SR) + len(seg)
        x = np.zeros((n, 2), np.float32)
        for h, nxt in zip(hits, hits[1:] + [None]):  # pad choke: a new hit cuts the last one (no stacking mud)
            p = int(round(h * beat * SR))
            k = len(seg) if nxt is None else min(len(seg), int(round(nxt * beat * SR)) - p)
            x[p: p + k] = declick(seg[:k].copy(), 48)
    if e.get("filter"):
        x = sweep(x, e["filter"])
    x = x * env(len(x), S(e.get("fade_in", 0)), S(e.get("fade_out", 0)))[:, None] * float(e.get("gain", 1))
    return x, n


def gap_bars(e) -> float:
    return float(e["bars"]) if e.get("bars") else float(e.get("beats", 2)) / 4


def repair_gaps(r: dict) -> dict:
    """A gap longer than 1 beat is dead air, not tension: shorten it to the last beat before the reveal and let
    whatever was playing into it run on (same source, continued) instead of burning a replan."""
    for g in [e for e in r["events"] if e["move"] == "gap"]:
        ln = gap_bars(g)
        if ln <= 0.25 + 1e-6:
            continue
        a0, a1 = float(g["at"]), float(g["at"]) + ln - 0.25
        for e in r["events"]:
            if e is not g and e["move"] in ("play", "loop") and abs(float(e["at"]) + float(e.get("bars", 1)) - a0) < 1e-6:
                e["bars"] = float(e.get("bars", 1)) + a1 - a0
        g.update(at=a1, bars=0.25)
        g.pop("beats", None)
    return r


def render_routine(r: dict, name: str, console=True, knobs=None) -> dict:
    M = float(r["master_bpm"])
    beat = 60.0 / M
    bar = 4 * beat
    S = lambda bars: int(round(bars * bar * SR))
    events = sorted(r["events"], key=lambda e: e["at"])
    used = {k: [e for e in events if e.get("deck") == k and e["move"] in ("play", "loop", "roll", "chop")] for k in r["decks"]}
    decks = {}
    for k, v in r["decks"].items():
        ev = used[k] or [{"src": 0}]
        lo = min(float(e.get("src", 0)) for e in ev)
        hi = max(float(e.get("src", 0)) + (e.get("bars", 1) if e["move"] == "play" else e.get("beats", 4) / 4) for e in ev) if used[k] else 1
        decks[k] = Deck(v, M, (int(lo), int(np.ceil(hi))))
        decks[k].prepare({s for e in used[k] for s in (e.get("stems") or STEM_NAMES) if s in STEM_NAMES})
    end = max(e["at"] + max(e.get("bars", 0), e.get("beats", 0) / 4, 0.25) for e in events) + 2
    L = S(end) + SR * 4
    bus = {(k, g): np.zeros((L, 2), np.float32) for k in decks for g in ("vox", "beat")} | {("fx", "fx"): np.zeros((L, 2), np.float32)}
    lanes = []

    def put(key, o, x):
        if 0 <= o < L:
            bus[key][o: o + len(x)] += x[: L - o]

    for e in events:
        mv, at = e["move"], float(e["at"])
        o = S(at)
        n0 = S(e.get("bars", 1))
        span = 1
        if mv in ("play", "loop", "roll", "chop"):
            d = decks[e["deck"]]
            names = [s for s in e.get("stems") or STEM_NAMES if s in STEM_NAMES]
            src = float(e.get("src", 0))
            for g, gn in (("vox", [s for s in names if s == "vocals"]), ("beat", [s for s in names if s != "vocals"])):
                if not gn:
                    continue
                x, n = render_move(e, events, d, gn, src, n0, S, beat, (e["deck"], g), o, put)
                put((e["deck"], g), o, x)
                if e.get("echo"):
                    put((e["deck"], g), o + len(x), render.echo_tail(x[-int(beat * SR):], int(beat * SR), S(2)) * 0.7)
                span = max(span, len(x))
        elif mv == "riser":
            put(("fx", "fx"), o, riser(n0))
            span = n0
        elif mv == "impact":
            put(("fx", "fx"), o, impact(int(2.5 * SR)))
            span = int(2.5 * SR)
        lanes.append({"start": at * bar, "end": at * bar + span / SR if mv not in ("gap", "tape_stop", "backspin")
                      else (at + (gap_bars(e) if mv == "gap" else e.get("beats", 2) / 4)) * bar,
                      "move": mv, "deck": e.get("deck"), "stems": e.get("stems"), "note": e.get("note", "")})

    mixrep = {}
    if console:  # closed-loop lock: measure each deck's real offset from the master grid in the mix, then cancel it
        mixrep["lock_ms"] = {}
        for k in decks:
            sig = bus[(k, "beat")] if np.abs(bus[(k, "beat")]).max() > 0 else bus[(k, "vox")]
            off = measure.grid_offset(sig, beat) if np.abs(sig).max() > 0 else 0.0
            sh = int(round(off / 1000 * SR))
            for g in ("vox", "beat"):
                bus[(k, g)] = np.roll(bus[(k, g)], -sh, axis=0)
            mixrep["lock_ms"][k] = round(-off, 1)
    mix = console_mix(bus, decks, beat, k=knobs or mixer_knobs, report=mixrep) if console else sum(bus.values())

    # master-bus moves, in time order, after everything is laid down
    for e in events:
        mv, o = e["move"], S(float(e["at"]))
        w = int(round(float(e.get("beats", 2)) * beat * SR))
        if mv == "gap":
            # planners write `bars` for gaps; and a pickup that starts inside the gap must not be muted with it
            a0 = float(e["at"])
            a1 = min([a0 + gap_bars(e)] + [float(q["at"]) for q in events if q is not e and a0 < float(q["at"]) < a0 + gap_bars(e)])
            w = S(a1 - a0)
            mix[o: o + w] *=np.r_[np.linspace(1, 0, 128), np.zeros(max(0, w - 256)), np.linspace(0, 1, 128)][: len(mix[o: o + w]), None]
        elif mv == "tape_stop":
            t = np.arange(w) / w
            read = o + (w * (t - t ** 2 / 2)).astype(int)  # speed ramps 1 -> 0
            seg = mix[np.clip(read, 0, len(mix) - 1)] * (1 - t[:, None] ** 3)
            mix[o: o + w] = seg[: len(mix) - o]
        elif mv == "backspin":
            t = np.arange(w) / w
            read = o - (2 * w * (t + t ** 2) / 2).astype(int)  # backwards, accelerating
            seg = mix[np.clip(read, 0, len(mix) - 1)] * (1 - t[:, None] ** 2)
            mix[o: o + w] = seg[: len(mix) - o]

    mix = mix[: S(end)]
    metrics = measure.report(bus, mix, events, bar, decks) | mixrep
    metrics["reward"] = measure.reward(metrics)  # redo with the console's post-match timbre residual
    peak = float(np.abs(mix).max())
    mix = render.master(mix)
    loud = np.flatnonzero(np.abs(mix).max(axis=1) > 1e-3)  # end on the last sound, not 4 s of padding
    mix = mix[: loud[-1] + SR // 2] if len(loud) else mix
    OUT.mkdir(parents=True, exist_ok=True)
    mp3 = OUT / f"{name}.mp3"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "2", "-i", "-",
                    "-b:a", "256k", str(mp3)], input=mix.astype(np.float32).tobytes(), check=True)
    wave = waveform(band_energy(np.ascontiguousarray(mix.mean(axis=1)[::2]), 512), 2400)
    res = {"name": name, "file": mp3.name, "duration": len(mix) / SR, "peak": peak, "waveform": wave,
           "bar_seconds": bar, "lanes": lanes, "routine": r, "metrics": metrics, "knobs": knobs or mixer_knobs,
           "decks": {k: {"id": d.meta["id"], "title": d.meta["title"], "stretch_pct": round((d.ratio - 1) * 100, 1),
                         "semitones": d.semitones} for k, d in decks.items()}}
    (OUT / f"{name}.json").write_text(json.dumps(res))
    return res


# ------------------------------------------------------------------ verifiable rewards for routines

def shifted_camelot(cam, semis):
    n, l = int(cam[:-1]), cam[-1]
    return f"{(n - 1 + 7 * int(round(semis))) % 12 + 1}{l}"


def check(r: dict) -> dict:
    v = []
    M = float(r["master_bpm"])
    metas = {k: stemlib.profile(d["id"]) for k, d in r["decks"].items()}
    ev = r["events"]
    end = max((e["at"] + e.get("bars", 1)) for e in ev)
    nbars = int(np.ceil(end * 4))  # beat resolution
    vocal = {k: np.zeros(nbars) for k in metas}
    bass = {k: np.zeros(nbars) for k in metas}
    harm = {k: np.zeros(nbars) for k in metas}
    sound = np.zeros(nbars)
    occ = {}

    for i, e in enumerate(ev):
        tag = f"E{i} {e['move']}@{e['at']}"
        if e["move"] not in MOVES:
            v.append(("SCHEMA", True, 1, 0, f"{tag}: unknown move"))
            continue
        if abs(e["at"] * 16 - round(e["at"] * 16)) > 1e-6:
            v.append(("Q1", True, 1, 0, f"{tag}: not on the 1/16 grid"))
        if e["move"] not in ("play", "loop", "roll", "chop"):
            if e["move"] in ("gap", "tape_stop", "backspin", "riser"):
                a, b = int(e["at"] * 4), int((e["at"] + (e.get("bars") or e.get("beats", 2) / 4)) * 4)
                sound[a:b] = 1
            continue
        d, m = r["decks"].get(e.get("deck")), metas.get(e.get("deck"))
        if not m:
            v.append(("SCHEMA", True, 1, 0, f"{tag}: unknown deck"))
            continue
        stems_ = e.get("stems") or list(STEM_NAMES)
        dur = e.get("bars", 1) if e["move"] != "chop" else (max(e.get("hits") or [0]) + e.get("beats", 1)) / 4
        src = float(e.get("src", 0))
        if src < 0 or src + (dur if e["move"] == "play" else e.get("beats", 4) / 4) > m["n_bars"]:
            v.append(("SCHEMA", True, 1, 0, f"{tag}: src bar out of range for {m['title'][:20]}"))
            continue
        if e["move"] == "play" and {"drums", "bass"} & set(stems_) and e["at"] % 1 and not e.get("fade_in"):
            v.append(("R1", True, 1, 0, f"{tag}: drums/bass slam in off the downbeat"))
        if e["move"] == "play" and {"drums", "bass"} & set(stems_) and e["at"] % 4 and not e.get("fade_in"):
            v.append(("R1", True, 1, 0, f"{tag}: drums/bass enter mid-phrase (not on a 4-bar line): the groove change will feel jerky"))
        a, b = int(e["at"] * 4), int((e["at"] + dur) * 4)
        sound[a:b] = 1
        for s_ in stems_:
            o = occ.setdefault((e["deck"], s_), np.zeros(nbars))
            o[a:min(b, nbars)] += 1
        for j in range(a, min(b, nbars)):
            sb = src + (j - a) / 4 if e["move"] == "play" else src
            sbar = int(sb)
            if sbar >= m["n_bars"]:
                break
            if "vocals" in stems_ and e["move"] != "chop" and any(p["start_beat"] <= sb * 4 < p["end_beat"] for p in m["vocal_phrases"]):
                vocal[e["deck"]][j] = 1
            if "bass" in stems_ and m["stem_profile"]["bass"][sbar] > 0.25:
                bass[e["deck"]][j] = 1
            if {"other", "vocals"} & set(stems_):
                harm[e["deck"]][j] = 1

    for (k, s_), o in occ.items():
        if (o > 1).any():
            v.append(("DUP", True, 1, 0, f"deck {k} {s_} plays twice at once for {int((o > 1).sum())} beats (two src positions = mud)"))
    keys = list(metas)
    if len(keys) >= 2:
        A, B = keys[:2]
        vo = int(((vocal[A] > 0) & (vocal[B] > 0)).sum())
        if vo > 4:
            v.append(("R16", True, 1, 0, f"two lead vocals overlap for {vo} beats"))
        elif vo:
            v.append(("R16", False, 3, 0.5, f"vocals overlap for {vo} beats"))
        bo = int(((bass[A] > 0) & (bass[B] > 0)).sum())
        if bo > 4:
            v.append(("R10", True, 1, 0, f"two basslines together for {bo} beats"))
        ho = int(((harm[A] > 0) & (harm[B] > 0)).sum())
        ca = shifted_camelot(metas[A]["camelot"], r["decks"][A].get("semitones", 0))
        cb = shifted_camelot(metas[B]["camelot"], r["decks"][B].get("semitones", 0))
        rel = rules.camelot_relation(ca, cb)
        if ho >= 8 and rules.KEY_SCORE[rel] < 1:
            v.append(("R18", False, 3, rules.KEY_SCORE[rel], f"{ca} vs {cb} ({rel}) under {ho} beats of melodic overlap; try semitones"))
    for k, d in r["decks"].items():
        mult = float(d.get("tempo_mult", 1))
        s = abs(M / (metas[k]["bpm"] * mult) - 1)
        if s > 0.18:
            v.append(("R22", True, 1, 0, f"deck {k} stretched {s:.0%}: it will sound broken (max 18%, or use tempo_mult 0.5/2)"))
        elif s > 0.10:
            v.append(("R22", False, 2, 0.6, f"deck {k} stretched {s:.0%}: fine on vocals, risky on full drums"))
        if abs(float(d.get("semitones", 0))) > 2:
            v.append(("R21", True, 1, 0, f"deck {k} pitched {d['semitones']} semitones: chipmunk territory (max 2)"))
    if all(float(d.get("semitones", 0)) for d in r["decks"].values()):
        v.append(("R21", True, 1, 0, "both decks pitch-shifted: shift one deck only (the vocal one), the other stays untouched"))
    for i, e in enumerate(ev):
        if e["move"] == "chop" and float(e.get("beats", 1)) > 1:
            v.append(("R30", False, 2, 0.5, f"E{i} chop@{e['at']}: {e['beats']}-beat slice is a phrase, not a chop; use 0.5-1 beat of one word"))
    dead = int((sound[: int(end * 4)] == 0).sum())
    if dead > 2:
        v.append(("AIR", True, 1, 0, f"{dead} beats of dead air"))
    used = {e["move"] for e in ev}
    if len(used) < 3:
        v.append(("R27", False, 2, 0.4, f"only {sorted(used)}: a routine needs more than one trick"))
    fx = sum(e["move"] in ("riser", "impact", "tape_stop", "backspin") for e in ev)
    if fx > 1:
        v.append(("R29", False, 2, 0.4, f"{fx} FX moves: cheesy, the reels use 0-1; let chops and vocal swaps do it"))
    secs = end * 4 * 60 / M
    if not 35 <= secs <= 75:
        v.append(("LEN", False, 1, 0.5, f"routine is {secs:.0f}s; a reel is 40-65s"))
    return rules.summarize(v)


if __name__ == "__main__":
    import sys
    r = json.loads(Path(sys.argv[1]).read_text())
    print(json.dumps(check(r), indent=1))
    res = render_routine(r, sys.argv[2] if len(sys.argv) > 2 else "routine_test")
    print(res["file"], round(res["duration"], 1), "s", res["decks"])
