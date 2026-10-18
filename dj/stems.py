"""Stem separation (Demucs htdemucs on the GPU) + exact per-bar stem activity.

stems(track_id) -> {"vocals": (n,2) float32, "drums": ..., "bass": ..., "other": ...} at 44.1 kHz, cached as .npy
profile(track_id) -> per-bar RMS of each stem and vocal phrases (bar/beat precise), cached into the analysis JSON
"""
import json
from pathlib import Path

import numpy as np

from analyze import CACHE

SR = 44100
DEMUCS = "htdemucs_ft"  # fine-tuned bag of 4: cleaner stems, less bleed/swirl than htdemucs (4x slower, cached)
STEMS = CACHE.parent / f"stems_{DEMUCS}"
NAMES = ("vocals", "drums", "bass", "other")
_MODEL = None


def separate(meta: dict) -> dict:
    global _MODEL
    import torch
    from demucs.apply import apply_model
    from demucs.pretrained import get_model
    from render import decode
    dev = "cuda" if torch.cuda.is_available() else "cpu"
    if _MODEL is None:
        _MODEL = get_model(DEMUCS).to(dev).eval()
    x = torch.from_numpy(decode(meta["path"]).T.copy())
    ref = x.mean(0)
    x = (x - ref.mean()) / ref.std()
    with torch.no_grad():
        out = apply_model(_MODEL, x[None], device=dev, split=True, overlap=0.25, progress=False)[0]
    out = out * ref.std() + ref.mean()
    return {name: out[i].T.contiguous().cpu().numpy().astype(np.float32) for i, name in enumerate(_MODEL.sources)}


def stems(track_id: str) -> dict:
    d = STEMS / track_id
    if not all((d / f"{n}.npy").exists() for n in NAMES):
        meta = json.loads((CACHE / f"{track_id}.json").read_text())
        d.mkdir(parents=True, exist_ok=True)
        for name, a in separate(meta).items():
            np.save(d / f"{name}.npy", a)
    return {n: np.load(d / f"{n}.npy", mmap_mode="r") for n in NAMES}


def profile(track_id: str) -> dict:
    """Per-bar loudness of each stem (0-1, track-relative) and vocal phrases with exact start/end bars."""
    path = CACHE / f"{track_id}.json"
    meta = json.loads(path.read_text())
    if meta.get("stems_model") == DEMUCS:
        return meta
    s = stems(track_id)
    db = np.array(meta["downbeats"])
    prof = {}
    for n in NAMES:
        a = np.asarray(s[n]).mean(axis=1)
        rms = np.array([np.sqrt(np.mean(a[int(t0 * SR):int(t1 * SR)] ** 2) + 1e-12) for t0, t1 in zip(db, db[1:])])
        prof[n] = np.round(rms / (rms.max() + 1e-9), 2).tolist()
    # vocal phrases at half-beat resolution: > -10 dB re the loud vocal level, single half-beat gaps bridged.
    # Dance tracks sing wall to wall, so a silence gate finds nothing; the breath between lines is a ~10 dB dip.
    a = np.asarray(s["vocals"]).mean(axis=1)
    hb = np.interp(np.arange(8 * (len(db) - 1)) / 8, np.arange(len(db)), db)
    hrms = np.array([np.sqrt(np.mean(a[int(t0 * SR):int(t1 * SR)] ** 2) + 1e-12) for t0, t1 in zip(hb, hb[1:])])
    on = 20 * np.log10(hrms / np.percentile(hrms, 95)) > -10
    on[1:-1] |= on[:-2] & on[2:]
    e = np.flatnonzero(np.diff(np.r_[0, on.astype(int), 0]))
    phrases = [{"start_beat": s0 / 2, "end_beat": s1 / 2, "start_bar": s0 / 8, "end_bar": s1 / 8}
               for s0, s1 in zip(e[::2].tolist(), e[1::2].tolist()) if s1 - s0 >= 4]
    meta["stem_profile"], meta["stems_model"] = prof, DEMUCS
    meta["vocal_phrases"] = phrases
    path.write_text(json.dumps(meta))
    return meta


if __name__ == "__main__":
    import sys
    import time
    for tid in sys.argv[1:]:
        t = time.time()
        m = profile(tid)
        print(f"{m['title'][:30]:30} {time.time() - t:5.1f}s  {len(m['vocal_phrases'])} vocal phrases:",
              [(p["start_bar"], p["end_bar"]) for p in m["vocal_phrases"][:12]])
