"""MOTH performs: stems + moves routines, planned by Gemini, checked by rules, judged by Gemini's ears."""
import json
import shutil
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import analyze
import learn
import lyrics
import render
import routine
import stems
from brain import CRIT_SCHEMA, FAST, PERSONA, SKILL, WEIGHTS, agy, job_dir, listen, log

EVENT = {"type": "object", "properties": {
    "at": {"type": "number", "description": "master bar (beat fractions .25/.5/.75 allowed)"},
    "move": {"type": "string", "enum": list(routine.MOVES)},
    "deck": {"type": "string", "enum": ["A", "B"]},
    "stems": {"type": "array", "items": {"type": "string", "enum": list(routine.STEM_NAMES)}},
    "src": {"type": "number", "description": "source bar in that deck's own numbering"},
    "bars": {"type": "number"}, "beats": {"type": "number"},
    "hits": {"type": "array", "items": {"type": "number"}, "description": "chop: beat offsets from at"},
    "filter": {"type": "string", "enum": ["lp_up", "lp_down", "hp_up", "hp_down"]},
    "fade_in": {"type": "number"}, "fade_out": {"type": "number"}, "gain": {"type": "number"},
    "echo": {"type": "boolean"}, "note": {"type": "string", "description": "why, in MOTH's voice"}},
    "required": ["at", "move", "note"]}

ROUTINE_SCHEMA = {"type": "object", "properties": {
    "title": {"type": "string", "description": "a name for this routine, like a DJ would caption the clip"},
    "story": {"type": "string", "description": "2-3 sentences in MOTH's voice: the idea of the routine"},
    "master_bpm": {"type": "number"},
    "decks": {"type": "object", "properties": {d: {"type": "object", "properties": {
        "semitones": {"type": "number"}, "tempo_mult": {"type": "number"}}} for d in ("A", "B")}},
    "events": {"type": "array", "items": EVENT}},
    "required": ["title", "story", "master_bpm", "decks", "events"]}

CRIT_SCHEMA_R = json.loads(json.dumps(CRIT_SCHEMA))
CRIT_SCHEMA_R["properties"]["scores"]["properties"]["performance"] = {"type": "integer"}
CRIT_SCHEMA_R["properties"]["scores"]["required"].append("performance")


def deck_sheet(m: dict) -> dict:
    p = m["stem_profile"]
    ears = m.get("ears", {})
    return {
        "id": m["id"], "title": m["title"], "bpm": m["bpm"], "key": m["key"], "camelot": m["camelot"],
        "n_bars": m["n_bars"], "bar_seconds": round(4 * m["beat_period"], 3),
        "ears": {k: ears.get(k) for k in ("genre", "language", "mood", "energy", "vibe", "warnings", "hooks")}
        | {"sections": [{k: s.get(k) for k in ("start_bar", "end_bar", "label", "vocals", "notes")} for s in ears.get("sections", [])]},
        "vocal_phrases_exact": [[ph["start_bar"], ph["end_bar"]] for ph in m["vocal_phrases"]],
        "lyrics_exact": {"legend": "start_bar: sung line (Whisper on the vocal stem; hooks' src_bar are grounded on these)",
                         "lines": [f"{ln['start_bar']:.2f}-{ln['end_bar']:.2f}: {ln['text']}" for ln in m.get("lyrics", [])]},
        "stems_per_bar_exact": {"legend": "bar: vocals drums bass other (0-1 loudness)",
                                "bars": [f"{b}: {p['vocals'][b]} {p['drums'][b]} {p['bass'][b]} {p['other'][b]}"
                                         for b in range(len(p["vocals"]))]},
    }


def plan(ids, brief, d, feedback=""):
    sheets = {k: deck_sheet(json.loads((analyze.CACHE / f"{i}.json").read_text())) for k, i in zip("AB", ids)}
    (d / "decks.json").write_text(json.dumps(sheets, indent=1, ensure_ascii=False), encoding="utf-8")
    (d / "lessons.json").write_text(json.dumps(learn.lessons(ids), indent=1, ensure_ascii=False), encoding="utf-8")
    prompt = f"""{PERSONA}

Read ROUTINES.md (how to perform a routine) and then decks.json: deck A and deck B, each with what your ears noted
(hooks, sections, vibe) and EXACT measurements from the separated stems (vocal phrases, per-bar stem loudness).
Trust the exact tables over your memory of timestamps: lyrics_exact says which words are sung at which bar.
Then read lessons.json: your past takes on similar pairs, best first, with what the user and the critic said.
Learn from them (repeat what scored, never repeat a named flaw), but don't copy them.

The request: "{brief}"

Write a routine of 40-65 seconds that a real person would replay, in the "oil and water" form from ROUTINES.md:
establish one record, then THE FLIP (its famous vocal on the other record's beat, key+tempo locked, on a downbeat,
8+ clean bars). Your creativity is the pairing: which vocal, which beat, which moment. Hook in the first 2 seconds,
famous moments only, long clean stretches, few moves (each one musical), FX 0 or 1. It must sound like one song.
Fewer events played well beat many events. Pitch-shift one deck at most, by as little as possible.
Hard rules: one lead vocal at a time (except chops), one bassline at a time, drums/bass enter on a downbeat (at = whole
number, ideally a multiple of 4), no dead air except one intentional gap, deck stretch at master_bpm <= 18% (use
tempo_mult 0.5/2 for half/double time), semitones within +/-2 to fix keys for melodic overlaps.
`at` is master bars from 0; `src` is the deck's own bar number; a play of N bars consumes N source bars.
{feedback}"""
    log("writing the routine ...")
    return agy(prompt, ROUTINE_SCHEMA, d)


def loudness(mp3: Path) -> str:
    """Per-second RMS so the critic can't hallucinate a '+23 dB blowout' (it did)."""
    import librosa
    import numpy as np
    y, sr = librosa.load(str(mp3), sr=22050)
    return " ".join(f"{t}s:{20 * np.log10(np.sqrt((y[t * sr:(t + 1) * sr] ** 2).mean()) + 1e-9):.0f}"
                    for t in range(len(y) // sr))


def critique(res: dict, d: Path, r: dict) -> dict:
    clip = d / res["file"]
    shutil.copy(render.OUT / res["file"], clip)
    moves = "\n".join(f"{e['at'] * res['bar_seconds']:.1f}s {e['move']} {e.get('deck', '')} {e.get('stems', '')}: {e['note']}"
                      for e in sorted(r["events"], key=lambda e: e["at"]))
    prompt = f"""{PERSONA}

You are now the harshest critic in the booth. Read RUBRIC.md and ROUTINES.md. First LISTEN to {', '.join(sorted(f.name for f in d.glob('ref_*.mp3')))} (in this folder): real
viral DJ reels the user loves. That is the bar. Then open {clip.name} with your file viewing tool and LISTEN to
the whole routine. Do not run commands. Judge it against the refs: is it as fun, as tight, as surprising?
The routine "{r['title']}": {r['story']}
Measured by the engine (trust these numbers; sync_ms > 10 is a flam, seam_db is the loudness jump at swaps):
{json.dumps({k: res["metrics"].get(k) for k in ("sync_ms", "vox_clarity_db", "seam_db", "flow_db")})}
Deck processing (stretch %, semitones; 0 semitones means NO pitch change, so no chipmunk): {json.dumps({k: [v["stretch_pct"], v["semitones"]] for k, v in res["decks"].items()})}
Loudness per second, dB RMS (a gap reads as silence): {loudness(clip)}
Never name a level or pitch flaw these numbers contradict.
Planned moves (time in this file):
{moves}

Score every rubric axis 1-10, plus `performance` (does this feel PLAYED, like a viral DJ clip, or like two songs
stitched?). Apply the caps. Name the single biggest flaw with its time, and the concrete fix (which move, which bar).
A 7 means a working DJ would post it. A 9 means people share it."""
    log("critic listening to the routine ...")
    c = agy(prompt, CRIT_SCHEMA_R, d, model=FAST)
    w = WEIGHTS | {"performance": .2}
    c["weighted"] = round(sum(w[k] * c["scores"].get(k, c["overall"]) for k in w) / sum(w.values()), 2)
    c["index"] = 0
    return c


def session(ids, brief, name, rounds=1, on_event=lambda *_: None) -> dict:
    on_event("stems", None)
    for i in ids:
        stems.profile(i)  # GPU separation, cached
    on_event("listen", None)
    with ThreadPoolExecutor(2) as ex:
        list(ex.map(lambda i: listen(i, need_hooks=True), ids))
    for i in ids:
        lyrics.lyrics(i)  # Whisper word timings; grounds the hooks Gemini heard
    d = job_dir(name)
    shutil.copy(SKILL.parent / "ROUTINES.md", d / "ROUTINES.md")
    for ref in (analyze.CACHE.parent.parent / "refs").glob("*.mp3"):  # reels the user loves: the critic's bar
        shutil.copy(ref, d / f"ref_{ref.name}")
    feedback, best, history = "", None, []
    for rnd in range(rounds + 2):  # one spare attempt for a hard-rule repair
        on_event("plan", rnd)
        r = plan(ids, brief, d, feedback)
        r["decks"] = {k: {**(r.get("decks", {}).get(k) or {}), "id": i} for k, i in zip("AB", ids)}
        for e in r["events"]:  # 7.88 means 7.875: snap to the 1/16-bar grid instead of burning a 4-minute replan
            e["at"] = round(float(e["at"]) * 16) / 16
        routine.repair_gaps(r)
        chk = routine.check(r)
        log(f"round {rnd}: rules {chk['score']}", [v["message"] for v in chk["violations"]])
        on_event("rules", chk)
        if any(v["hard"] for v in chk["violations"]):
            feedback = ("\nYOUR PREVIOUS ROUTINE FAILED THESE HARD RULES, fix every one:\n" +
                        "\n".join(f"- {v['message']}" for v in chk["violations"]) + f"\nPrevious routine: {json.dumps(r)}")
            continue
        on_event("render", rnd)
        kn = learn.knobs()
        res = routine.render_routine(r, f"{name}_v{rnd}", knobs=kn)
        on_event("critique", rnd)
        c = critique(res, d, r)
        learn.log_take(res["name"], ids, r, res["metrics"], chk["score"], critic=c["weighted"], knobs=kn,
                       flaw=c["biggest_flaw"], fix=c["fix"], brief=brief)
        v = {"round": rnd, "plan": r, "rules": chk, "mix": res, "critiques": [c], "score": c["weighted"]}
        history.append(v)
        log(f"round {rnd}: critic {c['weighted']} -> {c['biggest_flaw']}")
        if best is None or v["score"] > best["score"]:
            best = v
        if v["score"] >= 8 or len(history) > rounds:
            break
        feedback = (f"\nYou rendered it and listened back. Critic: {c['weighted']}/10. Flaw: {c['biggest_flaw']} "
                    f"Fix: {c['fix']}\nPrevious routine: {json.dumps(r)}\nRevise it. Keep what worked.")
    if best is None:
        raise RuntimeError("no routine passed the hard rules")
    out = {"best": best, "history": [{k: h[k] for k in ("round", "score")} for h in history]}
    (d / "result.json").write_text(json.dumps(out, indent=1))
    on_event("done", best)
    return out


if __name__ == "__main__":
    import sys
    res = session(sys.argv[1].split(","), sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else "routine_cli")
    b = res["best"]
    print(json.dumps({"title": b["plan"]["title"], "story": b["plan"]["story"], "file": b["mix"]["file"],
                      "score": b["score"], "history": res["history"], "critique": b["critiques"][0]}, indent=1))
