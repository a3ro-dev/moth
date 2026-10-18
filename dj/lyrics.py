"""Word-level lyrics on the beat grid (Whisper large-v3-turbo on the separated vocal stem).

lyrics(track_id) -> meta["lyrics"] = [{"text", "start_bar", "end_bar", "words": [{"w", "bar"}]}]  (one entry per sung line)
ground_hooks(meta) -> moves each of Gemini's hooks to where its words are actually sung (its timestamps are loose).
"""
import difflib
import json
import re

import numpy as np

import stems
from analyze import CACHE

SR = 44100
_MODEL = None


def to_bar(t, db):
    return float(np.interp(t, db, np.arange(len(db))))


def lyrics(track_id: str) -> dict:
    global _MODEL
    path = CACHE / f"{track_id}.json"
    meta = json.loads(path.read_text(encoding="utf-8"))
    if "lyrics" in meta:
        return meta
    import torch
    import whisper
    if _MODEL is None:
        _MODEL = whisper.load_model("turbo", device="cuda" if torch.cuda.is_available() else "cpu")
    v = np.asarray(stems.stems(track_id)["vocals"]).mean(axis=1)
    from scipy.signal import resample_poly
    v16 = resample_poly(v, 160, 441).astype(np.float32)  # 44.1k -> 16k
    # multilingual records (Portuguese + English, Hindi + English): detect per 30 s chunk, transcribe once per
    # language present, keep whichever transcription of each moment Whisper is more confident about
    langs = {}
    for o in range(0, len(v16) - 16000 * 5, 16000 * 30):
        mel = whisper.log_mel_spectrogram(whisper.pad_or_trim(v16[o:o + 16000 * 30]), _MODEL.dims.n_mels).to(_MODEL.device)
        _, probs = _MODEL.detect_language(mel)
        for lang, pr in probs.items():
            if pr > 0.25:
                langs[lang] = max(langs.get(lang, 0), pr)
    langs = sorted(langs, key=langs.get, reverse=True)[:2] or [None]
    segs = []
    for lang in langs:
        out = _MODEL.transcribe(v16, language=lang, word_timestamps=True, condition_on_previous_text=False,
                                no_speech_threshold=0.5, fp16=torch.cuda.is_available())
        segs += [s | {"lang": lang} for s in out["segments"]]
    segs.sort(key=lambda s: -s.get("avg_logprob", -9))
    kept = []
    for sg in segs:  # greedy: most confident first, drop anything overlapping a kept line by > 50%
        if all(min(sg["end"], k["end"]) - max(sg["start"], k["start"]) < 0.5 * (sg["end"] - sg["start"]) for k in kept):
            kept.append(sg)
    kept.sort(key=lambda s: s["start"])
    db = np.array(meta["downbeats"])
    lines = []
    for seg in kept:
        words = [{"w": w["word"].strip(), "bar": round(to_bar(w["start"], db), 3)} for w in seg.get("words", []) if w["word"].strip()]
        if not words:
            continue
        lines.append({"text": seg["text"].strip(), "start_bar": words[0]["bar"],
                      "end_bar": round(to_bar(seg["words"][-1]["end"], db), 3), "lang": seg["lang"], "words": words})
    meta["lyrics"], meta["lyrics_lang"] = lines, langs
    ground_hooks(meta)
    path.write_text(json.dumps(meta), encoding="utf-8")
    return meta


def norm(s):
    return re.sub(r"[^\w ]", "", s.lower()).split()


def ground_hooks(meta):
    """Find each hook in the transcript by how it SOUNDS (character match over word windows, so Whisper's
    'dick dick dick' still finds 'drift drift drift'); move src_bar only on a confident match near Gemini's guess."""
    ears = meta.get("ears") or {}
    words = [(w["bar"], t) for ln in meta.get("lyrics", []) for w in ln["words"] for t in norm(w["w"])[:1]]
    if not words:
        return
    toks = [t for _, t in words]
    for h in ears.get("hooks", []):
        h.pop("also_at", None)
        q = norm(re.sub(r"\(.*?\)", lambda m: m.group(0)[1:-1], h.get("words", "")))
        if not q or len(q) > 40:
            continue
        qs = " ".join(q)
        guess = float(h.get("src_bar_heard") if h.get("src_bar_heard") is not None else h.get("src_bar", 0))
        cands = []
        for i in range(len(toks)):
            for n in {max(1, len(q) - 1), len(q), len(q) + 1}:
                sc = difflib.SequenceMatcher(None, qs, " ".join(toks[i:i + n])).ratio()
                cands.append((sc, i))
        top = max(c[0] for c in cands)
        if top < 0.6:
            h["grounded"] = 0  # not found in the lyrics: keep Gemini's guess, flagged
            continue
        good = sorted({i for sc, i in cands if sc >= top - 0.05}, key=lambda i: abs(words[i][0] - guess))
        h["src_bar_heard"] = guess
        h["src_bar"] = round(words[good[0]][0], 3)
        h["grounded"] = round(top, 2)
        h["also_at"] = sorted({round(words[i][0], 2) for i in good[1:] if abs(words[i][0] - words[good[0]][0]) > 2})[:6]


if __name__ == "__main__":
    import sys
    import time
    for tid in sys.argv[1:]:
        t = time.time()
        m = lyrics(tid)
        print(f"{m['title'][:30]:30} {time.time() - t:5.1f}s lang={m['lyrics_lang']} lines={len(m['lyrics'])}")
        for ln in m["lyrics"][:12]:
            print(f"   bar {ln['start_bar']:7.2f}  {ln['text'][:70]}")
        for h in (m.get("ears") or {}).get("hooks", []):
            print(f"   HOOK {h['words'][:40]:40} heard@{h.get('src_bar_heard')} -> {h['src_bar']} ({h.get('grounded')}) also {h.get('also_at')}")
