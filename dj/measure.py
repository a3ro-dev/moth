"""Verifiable rewards for a rendered routine: the numbers behind 'oil and water'.

  sync_ms        median |timing offset| between decks where both play (onset-envelope cross-correlation). 0 = locked.
  grid_ms        per deck, median offset of its onsets from the master beat grid.
  vox_clarity_db vocal presence over the beat in 1-5 kHz while a vocal plays (higher = sits on top, < 0 = buried).
  timbre_mismatch_db  tonal-balance (LTAS) distance between a vocal's native beat and the foreign beat under it (lower = one record).
  seam_db      mean / max jump in short-term loudness across every event boundary (lower = smoother).
  flow_db        std of 400 ms loudness over the clip, gaps excluded (lower = steadier energy).
reward() folds them into 0-1, so the learning loop can compare takes and engine settings.
"""
import numpy as np
from mixer import band, rms_env, timbre_gap, timbre_pairs

SR = 44100
HOP = 128  # 2.9 ms


def onset_env(x):
    """Transient envelope with no look-ahead: log energy of the pre-emphasized signal per 2.9 ms frame, rising edges.
    (librosa's onset_strength uses a centered 2048-point window and fires ~20 ms early: useless for ms-level sync.)"""
    m = x.mean(axis=1) if x.ndim == 2 else x
    m = np.diff(m.astype(np.float64), prepend=0)
    n = len(m) // HOP
    e = np.log10((m[: n * HOP].reshape(n, HOP) ** 2).mean(axis=1) + 1e-10)
    return np.maximum(0, np.diff(e, prepend=e[0]))


def best_lag(a, b, max_ms=40):
    """Lag (ms) of b relative to a maximizing correlation of their onset envelopes."""
    k = int(max_ms / 1000 * SR / HOP)
    a, b = a - a.mean(), b - b.mean()
    lags = range(-k, k + 1)
    c = [float(np.dot(a[max(0, l): len(a) + min(0, l)], b[max(0, -l): len(b) - max(0, l)])) for l in lags]
    return lags[int(np.argmax(c))] * HOP / SR * 1000, max(c) / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-9)


def grid_offset(x, beat_s, t0=0.0):
    """Median ms offset of onsets from beat positions t0 + k*beat (positive = late)."""
    e = onset_env(x)
    k = int(0.04 * SR / HOP)
    beats = np.arange(t0, len(x) / SR - 0.05, beat_s)
    offs = []
    for b in beats:
        i = int(b * SR / HOP)
        w = e[max(0, i - k): i + k + 1]
        if len(w) == 2 * k + 1 and w.max() > np.percentile(e, 75):
            offs.append((int(np.argmax(w)) - k) * HOP / SR * 1000)
    return float(np.median(offs)) if offs else 0.0


def report(bus, mix, events, bar, decks):
    beat = bar / 4
    L = len(mix)
    r = {}
    deck_sig = {d: bus[(d, "vox")] + bus[(d, "beat")] for d in decks}
    # sync between decks, in 2-bar windows where both are loud
    w = int(2 * bar * SR)
    keys = list(decks)
    lags = []
    if len(keys) >= 2:
        A, B = deck_sig[keys[0]], deck_sig[keys[1]]
        for o in range(0, L - w, w):
            a, b = A[o:o + w], B[o:o + w]
            if np.abs(a).mean() > 1e-3 and np.abs(b).mean() > 1e-3:
                lag, c = best_lag(onset_env(a), onset_env(b))
                if c > 0.1:
                    lags.append(abs(lag))
    r["sync_ms"] = round(float(np.median(lags)), 1) if lags else None
    r["grid_ms"] = {d: round(grid_offset(deck_sig[d], beat), 1) for d in keys if np.abs(deck_sig[d]).max() > 0}
    # vocal clarity
    vox = sum(bus[(d, "vox")] for d in keys)
    bt = sum(bus[(d, "beat")] for d in keys)
    ve, be = rms_env(band(vox, 1000, 5000), 0.1), rms_env(band(bt, 1000, 5000), 0.1)
    on = ve > 0.2 * ve.max() if ve.max() > 0 else np.zeros(L, bool)
    r["vox_clarity_db"] = round(float(np.median(20 * np.log10(ve[on] / (be[on] + 1e-9)))), 1) if on.any() else None
    # timbre: raw bus here; the console overwrites it with the post-match residual (routine.py)
    r["timbre_mismatch_db"] = timbre_gap(timbre_pairs(decks, {d: bus[(d, "vox")] for d in keys}, {d: bus[(d, "beat")] for d in keys}))
    # seams
    loud = 20 * np.log10(np.maximum(rms_env(mix, 0.05), 1e-3))  # floor at -60 dB: silence isn't a 100 dB "jump"
    # swap points: where one part ends and another begins (that's where a mix feels jerky), not every entry
    ends = {round(float(e["at"]) + float(e.get("bars", 0)), 4) for e in events if e["move"] == "play"}
    starts = {round(float(e["at"]), 4) for e in events if e["move"] == "play"}
    seams = sorted(ends & starts)
    gaps = [(float(e["at"]), float(e["at"]) + float(e.get("bars") or float(e.get("beats", 2)) / 4)) for e in events if e["move"] == "gap"]
    in_gap = lambda t: any(a - 0.05 <= t <= b + 0.05 for a, b in gaps)
    d50 = int(0.05 * SR)
    jumps = [abs(loud[min(L - 1, int(t * bar * SR) + d50)] - loud[max(0, int(t * bar * SR) - d50)])
             for t in seams if 0.1 < t * bar < L / SR - 1 and not in_gap(t)]
    r["seam_db"] = {"mean": round(float(np.mean(jumps)), 1), "max": round(float(np.max(jumps)), 1)} if jumps else None
    st =20 * np.log10(rms_env(mix, 0.4)[:: int(0.1 * SR)] + 1e-9)
    st = st[st > st.max() - 30]
    r["flow_db"] = round(float(np.std(st)), 1)
    r["reward"] = reward(r)
    return r


def reward(r):
    """0-1. Each term is 1 when perfect and decays where listeners start to notice."""
    terms = []
    if r.get("sync_ms") is not None:
        terms.append(np.exp(-r["sync_ms"] / 10))  # 10 ms ~ the flam threshold
    if r.get("grid_ms"):
        terms.append(np.exp(-np.mean([abs(v) for v in r["grid_ms"].values()]) / 10))
    if r.get("vox_clarity_db") is not None:
        terms.append(1 / (1 + np.exp(-(r["vox_clarity_db"] - 0) / 2)))
    if r.get("timbre_mismatch_db") is not None:
        terms.append(np.exp(-r["timbre_mismatch_db"] / 4))  # ~4 dB average tonal-balance gap = obviously a different record
    if r.get("seam_db"):
        terms.append(np.exp(-r["seam_db"]["mean"] / 6))
    terms.append(np.exp(-max(0, r["flow_db"] - 3) / 3))
    return round(float(np.mean(terms)), 3)
