"""Track dissection: everything a DJ reads off the screen before touching a fader.

Beat grid, downbeats, phrases, key (Camelot), loudness, per-bar energy by band,
coarse sections, a 3-band waveform for the UI and a timbre vector for QenloDB.
"""
import hashlib
import json
import subprocess
import sys
from pathlib import Path

import librosa
import numpy as np
import pyloudnorm

SR = 22050
CACHE = Path(__file__).resolve().parent.parent / "data" / "analysis"

# Krumhansl-Kessler key profiles
MAJOR = np.array([6.35, 2.23, 3.48, 2.33, 4.38, 4.09, 2.52, 5.19, 2.39, 3.66, 2.29, 2.88])
MINOR = np.array([6.33, 2.68, 3.52, 5.38, 2.60, 3.53, 2.54, 4.75, 3.98, 2.69, 3.34, 3.17])
NAMES = ["C", "C#", "D", "Eb", "E", "F", "F#", "G", "Ab", "A", "Bb", "B"]


def camelot(pc: int, minor: bool) -> str:
    major_pc = (pc + 3) % 12 if minor else pc
    return f"{(major_pc * 7 % 12 + 7) % 12 + 1}{'A' if minor else 'B'}"


def track_id(path: Path) -> str:
    return hashlib.sha1(str(path.resolve()).encode()).hexdigest()[:12]


def load(path: Path, sr=SR) -> np.ndarray:
    """Decode anything ffmpeg understands to mono float32."""
    raw = subprocess.run(
        ["ffmpeg", "-v", "error", "-i", str(path), "-ac", "1", "-ar", str(sr), "-f", "f32le", "-"],
        capture_output=True, check=True).stdout
    return np.frombuffer(raw, dtype=np.float32).copy()


def detect_key(y):
    chroma = librosa.feature.chroma_cqt(y=y, sr=SR).mean(axis=1)
    best = max(((np.corrcoef(chroma, np.roll(prof, pc))[0, 1], pc, minor)
                for pc in range(12) for minor, prof in ((False, MAJOR), (True, MINOR))))
    score, pc, minor = best
    return {"key": NAMES[pc] + ("m" if minor else ""), "camelot": camelot(pc, minor),
            "key_confidence": round(float(score), 3)}


_BEATS = None


def beat_grid(y, duration):
    """Beat This! (CPJKU 2024) beats + downbeats. Bars are real downbeat-to-downbeat spans, so
    drifting live/Bollywood tempos stay on grid. Downbeats are extrapolated over beatless intros/outros."""
    global _BEATS
    if _BEATS is None:
        from beat_this.inference import Audio2Beats
        _BEATS = Audio2Beats(checkpoint_path="small0", device="cpu", dbn=False)
    beats, downs = (np.asarray(x, dtype=float) for x in _BEATS(y, SR))
    # one metrical level: beat period folded into 80-160 BPM (rekordbox default range); the model
    # flips between half/double time across sections in hip-hop and desi tracks
    period = float(np.median(np.diff(beats)))
    while period > 0.75:
        period /= 2
    while period < 0.375:
        period *= 2
    bar = 4 * period
    # rebuild downbeats on that level: fill skipped bars, drop spurious ones, keep local tempo
    grid = [downs[0]]
    for d in downs[1:]:
        n = int(round((d - grid[-1]) / bar))
        if n == 0:
            continue
        grid += list(grid[-1] + (d - grid[-1]) * np.arange(1, n + 1) / n)
    downs = np.array(grid)
    grid_conf = float(np.mean(np.abs(np.diff(downs) / bar - 1) < 0.06))
    period = float(np.median(np.diff(downs))) / 4  # frame-quantised beats are coarse; bars average it out
    bar = 4 * period
    pre = downs[0] - bar * np.arange(int(downs[0] // bar), 0, -1)
    post = downs[-1] + bar * np.arange(1, int((duration - downs[-1]) // bar) + 1)
    downs_full = np.concatenate([pre, downs, post])
    grid_beats = np.interp(np.arange(4 * (len(downs_full) - 1)) / 4, np.arange(len(downs_full)), downs_full)
    return 60.0 / period, period, downs_full, grid_beats, grid_conf


def band_energy(y, hop):
    S = np.abs(librosa.stft(y, n_fft=2048, hop_length=hop))
    f = librosa.fft_frequencies(sr=SR, n_fft=2048)
    bands = [(0, 200), (200, 2500), (2500, SR / 2)]
    return np.stack([np.sqrt((S[(f >= lo) & (f < hi)] ** 2).mean(axis=0)) for lo, hi in bands])


def waveform(bands, cols=1200):
    """3-band (low/mid/high) peak waveform for the UI, normalised to 0..1."""
    edges = np.linspace(0, bands.shape[1], cols + 1).astype(int)
    wave = [[float(bands[i, a:b].max()) if b > a else 0.0 for a, b in zip(edges, edges[1:])] for i in range(3)]
    wmax = max(max(w) for w in wave) or 1.0
    return [[round(v / wmax, 3) for v in w] for w in wave]


def analyze(path: str | Path, force=False) -> dict:
    path = Path(path)
    tid = track_id(path)
    out = CACHE / f"{tid}.json"
    if out.exists() and not force:
        return json.loads(out.read_text())

    y = load(path)
    duration = len(y) / SR
    bpm, period, downbeats, beats, grid_conf = beat_grid(y, duration)
    n_bars = len(downbeats) - 1
    bar_starts = downbeats[:-1]
    bar_ends = downbeats[1:]

    # per-bar energy by band (low/mid/high), normalised to the track's own max
    hop = 512
    bands = band_energy(y, hop)
    t = librosa.frames_to_time(np.arange(bands.shape[1]), sr=SR, hop_length=hop)
    per_bar = np.stack([bands[:, (t >= s) & (t < e)].mean(axis=1) for s, e in zip(bar_starts, bar_ends)]) if n_bars else np.zeros((0, 3))
    per_bar = per_bar / (per_bar.max(axis=0, keepdims=True) + 1e-9)
    energy = per_bar.mean(axis=1)

    # coarse sections: agglomerative clustering over bar features, snapped to 4-bar boundaries
    sections = []
    if n_bars >= 16:
        mfcc = librosa.feature.mfcc(y=y, sr=SR, n_mfcc=13, hop_length=hop)
        tm = librosa.frames_to_time(np.arange(mfcc.shape[1]), sr=SR, hop_length=hop)
        feat = np.stack([mfcc[:, (tm >= s) & (tm < e)].mean(axis=1) for s, e in zip(bar_starts, bar_ends)]).T
        feat = np.vstack([librosa.util.normalize(feat, axis=1), per_bar.T * 3])
        k = max(4, n_bars // 16)
        bounds = librosa.segment.agglomerative(feat, k)
        bounds = sorted({0, n_bars, *[min(n_bars, int(round(b / 4) * 4)) for b in bounds]})
        q = np.quantile(energy, [0.33, 0.66])
        for a, b in zip(bounds, bounds[1:]):
            if b <= a:
                continue
            e = float(energy[a:b].mean())
            sections.append({"start_bar": a, "end_bar": b, "start": float(bar_starts[a]),
                             "energy": round(e, 3),
                             "level": "low" if e < q[0] else "high" if e > q[1] else "mid",
                             "low_end": round(float(per_bar[a:b, 0].mean()), 3)})

    wave = waveform(bands)

    # timbre/groove vector for similarity search in QenloDB
    mf = librosa.feature.mfcc(y=y, sr=SR, n_mfcc=20).mean(axis=1)
    contrast = librosa.feature.spectral_contrast(y=y, sr=SR).mean(axis=1)
    chroma = librosa.feature.chroma_cqt(y=y, sr=SR).mean(axis=1)
    key = detect_key(y)
    tempo_feat = [np.sin(2 * np.pi * np.log2(bpm / 60)), np.cos(2 * np.pi * np.log2(bpm / 60))]  # octave-invariant
    vec = np.concatenate([mf / (np.linalg.norm(mf) + 1e-9), contrast / (np.linalg.norm(contrast) + 1e-9),
                          chroma / (np.linalg.norm(chroma) + 1e-9), tempo_feat, [energy.mean() if n_bars else 0]])
    vec = vec / (np.linalg.norm(vec) + 1e-9)

    result = {
        "id": tid, "path": str(path.resolve()), "title": path.stem, "duration": round(duration, 3),
        "bpm": round(bpm, 2), "beat_period": period, "grid_confidence": round(grid_conf, 3),
        "n_bars": n_bars, "beats": [round(float(b), 4) for b in beats],
        "downbeats": [round(float(b), 4) for b in downbeats],
        "lufs": round(float(pyloudnorm.Meter(SR).integrated_loudness(y.astype(np.float64))), 2),
        **key,
        "bar_energy": [[round(float(v), 3) for v in row] for row in per_bar],
        "sections": sections, "waveform": wave, "vector": [round(float(v), 5) for v in vec],
    }
    CACHE.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result))
    return result


if __name__ == "__main__":
    assert camelot(0, False) == "8B" and camelot(9, True) == "8A" and camelot(7, False) == "9B" and camelot(0, True) == "5A"
    for p in sys.argv[1:]:
        r = analyze(p, force=True)
        print(f"{r['title'][:40]:40} {r['bpm']:7.2f} BPM grid {r['grid_confidence']:.2f}  {r['key']:4} {r['camelot']:4} {r['lufs']:6.1f} LUFS  "
              f"{r['n_bars']} bars  {len(r['sections'])} sections")
