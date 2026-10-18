"""MOTH's brain: Gemini (via the Antigravity CLI) listens, plans, and judges.

listen(track)  -> Gemini hears the whole track once, annotates vocals/sections/cue points (cached)
plan(...)      -> mix plan JSON, grounded in skills/dj-craft/SKILL.md + DSP data
critique(...)  -> Gemini listens to each rendered transition and scores it with the skill's rubric
session(...)   -> plan -> rule check -> render -> listen -> revise, keeping the best version
"""
import json
import shutil
import subprocess
import time
from pathlib import Path

import analyze
import render
import rules

ROOT = Path(__file__).resolve().parent.parent
SKILL = ROOT / "skills" / "dj-craft" / "SKILL.md"
JOBS = ROOT / "data" / "jobs"
MODEL = "gemini-3.8-flash-high"  # planning: taste lives here
FAST = "gemini-3.8-flash-medium"  # listening + critique: perception, not deliberation (tier is in the name; agy rejects --effort with it)

PERSONA = """You are MOTH, a nocturnal DJ who has played a thousand nights. You are drawn to the lights of a
good dancefloor and allergic to trainwrecks. Your taste is restrained and deliberate: you would rather do
one perfect transition than three flashy ones, you respect phrasing like scripture, you never let two vocals
fight, and you pick the obvious-in-hindsight move for each pair of tracks. You talk like a real DJ: short,
dry, specific, a little warm. Nobody should ever suspect a machine made your mix."""


def log(*a):
    print(time.strftime("%H:%M:%S"), *a, flush=True)


def agy(prompt: str, schema: dict, cwd: Path, timeout=900, model=MODEL) -> dict:
    """One Gemini turn in a sandboxed job folder. Plan mode: it can read files and hear audio, but runs no commands."""
    (cwd / "schema.json").write_text(json.dumps(schema))
    prompt = ("TOOLS: use ONLY your file viewing/reading tool (it reads text and plays audio natively). Never run shell "
              "commands or scripts: they are blocked and your turn will fail.\n\n" + prompt)
    for attempt in range(3):
        p = subprocess.run(["agy", "-p", prompt, "--model", model, "--mode", "plan", "--output-format", "json",
                            "--json-schema", "schema.json", "--print-timeout", f"{timeout}s"],
                           cwd=cwd, capture_output=True, text=True, encoding="utf-8", timeout=timeout + 60)
        lines = [l for l in p.stdout.splitlines() if l.startswith("{")]
        if lines:
            out = json.loads(lines[-1])
            if out.get("structured_output"):
                return out["structured_output"]
        log(f"agy attempt {attempt + 1} gave no structured output: {(p.stdout + p.stderr)[-400:]}")
    raise RuntimeError("Gemini did not return structured output")


def job_dir(name: str) -> Path:
    d = JOBS / name
    d.mkdir(parents=True, exist_ok=True)
    for f in ("SKILL.md", "CORE.md", "RUBRIC.md"):
        shutil.copy(SKILL.parent / f, d / f)
    return d


# ---------------------------------------------------------------- listening

EARS_SCHEMA = {
    "type": "object",
    "properties": {
        "genre": {"type": "string"}, "language": {"type": "string"},
        "mood": {"type": "string"}, "energy": {"type": "integer", "description": "1-10 dancefloor energy"},
        "vibe": {"type": "string", "description": "one vivid line a DJ would say about this record"},
        "sections": {"type": "array", "items": {"type": "object", "properties": {
            "start_s": {"type": "number"}, "end_s": {"type": "number"},
            "label": {"type": "string", "description": "intro|verse|pre-chorus|hook|chorus|drop|breakdown|bridge|instrumental|outro"},
            "vocals": {"type": "boolean"}, "notes": {"type": "string"}},
            "required": ["start_s", "end_s", "label", "vocals"]}},
        "mix_in": {"type": "array", "items": {"type": "object", "properties": {
            "bar": {"type": "integer"}, "why": {"type": "string"}}, "required": ["bar", "why"]}},
        "mix_out": {"type": "array", "items": {"type": "object", "properties": {
            "bar": {"type": "integer"}, "why": {"type": "string"}}, "required": ["bar", "why"]}},
        "warnings": {"type": "string", "description": "anything that makes this track hard to mix"},
        "hooks": {"type": "array", "description": "the recognizable, chop-able moments: signature words, the riff everyone knows",
                  "items": {"type": "object", "properties": {
                      "phrase": {"type": "integer", "description": "index into the vocal phrase table, or -1 for an instrumental riff"},
                      "src_bar": {"type": "number", "description": "exact start in bars (beat fractions .25/.5/.75 allowed)"},
                      "beats": {"type": "number", "description": "length of the chop-able bit in beats"},
                      "words": {"type": "string"}, "why": {"type": "string"}},
                      "required": ["src_bar", "beats", "words"]}},
    },
    "required": ["genre", "language", "mood", "energy", "vibe", "sections", "mix_in", "mix_out", "warnings", "hooks"],
}


def listen(track_id: str, need_hooks=False) -> dict:
    meta = json.loads((analyze.CACHE / f"{track_id}.json").read_text())
    if "ears" in meta and (not need_hooks or "hooks" in meta["ears"]):
        return meta
    d = job_dir(f"listen_{track_id}")
    src = Path(meta["path"])
    audio = d / f"track{src.suffix}"
    shutil.copy(src, audio)
    e = meta["bar_energy"]
    avg = lambda b, k: sum(r[k] for r in e[b:b + 4]) / len(e[b:b + 4])
    grid = "\n".join(f"bar {b}: {t:.2f}s  low {avg(b, 0):.2f} mid {avg(b, 1):.2f} high {avg(b, 2):.2f}"
                     for b, t in enumerate(meta["downbeats"]) if b % 4 == 0 and b < len(e))
    phrases = "\n".join(f"phrase {i}: bars {p['start_bar']}-{p['end_bar']} ({meta['downbeats'][int(p['start_bar'])]:.1f}s)"
                        for i, p in enumerate(meta.get("vocal_phrases", [])))
    prompt = f"""{PERSONA}

Open {audio.name} with your file viewing tool and LISTEN to the whole record carefully. Do not run commands.
Title: {meta['title']}. Measured: {meta['bpm']} BPM, key {meta['key']} ({meta['camelot']}), {meta['duration']:.0f}s.
Below: the downbeat grid (bar -> time) with MEASURED band energy for the next 4 bars (low = kick/bass, mid =
vocals/instruments, high = hats). Your sense of time in long audio is approximate; these numbers are exact. Snap
every section boundary to where the measured energy actually changes (drums enter where low jumps).
{grid}
{"Vocal phrases, measured exactly from the isolated vocal stem (bars, with beat fractions):" + chr(10) + phrases if phrases else ""}

Annotate it like a DJ prepping a USB before a gig: every section with its time range and whether lead vocals
are present; where you would bring this track in (mix_in) and take it out (mix_out) on phrase boundaries; and the
HOOKS: the recognizable words/riffs a DJ would chop, loop or tease (name the phrase index and the exact src_bar of
the word, and say the words). Be precise about vocals, they decide everything."""
    log(f"listening to {meta['title']} ...")
    ears = agy(prompt, EARS_SCHEMA, d, model=FAST, timeout=600)
    db = meta["downbeats"]
    to_bar = lambda t: min(range(len(db)), key=lambda i: abs(db[i] - t))
    ears["vocal_bars"] = [[to_bar(s["start_s"]), to_bar(s["end_s"])] for s in ears["sections"] if s.get("vocals")]
    for s in ears["sections"]:
        s["start_bar"], s["end_bar"] = to_bar(s["start_s"]), to_bar(s["end_s"])
    meta["ears"] = ears
    (analyze.CACHE / f"{track_id}.json").write_text(json.dumps(meta))
    return meta


# ---------------------------------------------------------------- planning

PLAN_SCHEMA = {
    "type": "object",
    "properties": {
        "story": {"type": "string", "description": "2-3 sentences, in MOTH's voice, on the arc of this mix"},
        "tracks": {"type": "array", "items": {"type": "object", "properties": {
            "id": {"type": "string"}, "cue_in_bar": {"type": "integer"}}, "required": ["id", "cue_in_bar"]}},
        "transitions": {"type": "array", "items": {"type": "object", "properties": {
            "start_bar": {"type": "integer", "description": "bar in the OUTGOING track where the incoming track's cue_in_bar lands"},
            "bars": {"type": "integer", "description": "overlap length: 0 cut, 1-2 echo tail, else 4/8/16/32"},
            "type": {"type": "string", "enum": sorted(render.TYPES)},
            "swap_at": {"type": "number", "description": "0.25|0.5|0.75: where in the overlap the bass swaps"},
            "energy_boost": {"type": "boolean"},
            "why": {"type": "string", "description": "one line, MOTH's voice"}},
            "required": ["start_bar", "bars", "type", "why"]}},
    },
    "required": ["story", "tracks", "transitions"],
}


def summary(m: dict) -> dict:
    e = m["bar_energy"]
    return {
        "id": m["id"], "title": m["title"], "bpm": m["bpm"], "key": m["key"], "camelot": m["camelot"],
        "grid_confidence": m["grid_confidence"], "n_bars": m["n_bars"], "duration_s": round(m["duration"]),
        "bar_seconds": round(4 * m["beat_period"], 3),
        "energy_per_4_bars": [round(sum(sum(r) / 3 for r in e[i:i + 4]) / len(e[i:i + 4]), 2) for i in range(0, len(e), 4)],
        "dsp_sections": [{k: s[k] for k in ("start_bar", "end_bar", "level")} for s in m["sections"]],
        "ears": {k: m["ears"][k] for k in ("genre", "language", "mood", "energy", "vibe", "mix_in", "mix_out", "warnings")}
        | {"sections": [{k: s.get(k) for k in ("start_bar", "end_bar", "label", "vocals", "notes")} for s in m["ears"]["sections"]]},
    }


def plan(ids: list[str], brief: str, d: Path, feedback: str = "", keep_order=True) -> dict:
    metas = [listen(i) for i in ids]
    (d / "tracks.json").write_text(json.dumps([summary(m) for m in metas], indent=1))
    order = "Play them in the given order." if keep_order else "Choose the order (and drop tracks that don't belong) for the best arc."
    prompt = f"""{PERSONA}

Read CORE.md first: it is your craft (taste, phrasing, cue rules, transition choice, slop detectors).
Then read tracks.json: every track's measured grid, energy and what your own ears noted.

The request: "{brief}"
{order}

Write the mix plan. Rules of thumb you never break: enter and exit on phrase boundaries (bar multiple of 8 or a
section start, in that track's own bar numbers), never overlap two lead vocals for more than 1 bar, one bassline at a time,
beatmatched types (blend/bass_swap/eq_swap/filter) only when tempos are within 6% and both grids are confident (>=0.8),
otherwise echo_out or cut. Let each record play its best section before you leave it. Vary your transitions.
The renderer is literal: tracks[i+1].cue_in_bar is placed exactly on transitions[i].start_bar of tracks[i], and the
outgoing track is gone after start_bar + bars (or immediately at start_bar for cut/echo_out).
{feedback}"""
    log("planning ...")
    return agy(prompt, PLAN_SCHEMA, d)


# ---------------------------------------------------------------- critique

CRIT_SCHEMA = {
    "type": "object",
    "properties": {
        "scores": {"type": "object", "properties": {k: {"type": "integer"} for k in (
            "beat_sync", "phrase_fit", "low_end", "harmony", "vocals", "level", "clarity", "choice", "fx",
            "selection", "human_feel", "floor")}, "required": ["beat_sync", "phrase_fit", "low_end", "vocals", "human_feel"]},
        "overall": {"type": "number", "description": "weighted per the rubric, after caps, 1-10"},
        "biggest_flaw": {"type": "string"}, "flaw_at_s": {"type": "number"},
        "fix": {"type": "string", "description": "the concrete change an experienced DJ would make (bars, type, cue)"},
        "verdict": {"type": "string", "description": "one line in MOTH's voice"},
    },
    "required": ["scores", "overall", "biggest_flaw", "fix", "verdict"],
}

WEIGHTS = {"beat_sync": .15, "phrase_fit": .12, "low_end": .12, "harmony": .08, "vocals": .08, "level": .08,
           "clarity": .06, "choice": .08, "fx": .05, "selection": .08, "human_feel": .07, "floor": .03}


def critique(mix: dict, d: Path) -> list[dict]:
    out = []
    for w in mix["transitions"]:
        clip = d / w["clip"]
        shutil.copy(render.OUT / w["clip"], clip)
        tl = mix["timeline"]
        a, b = tl[w["index"]], tl[w["index"] + 1]
        rel0, rel1 = w["mix_start"] - w["clip_offset"], w["mix_end"] - w["clip_offset"]
        prompt = f"""{PERSONA}

You are now the harshest critic in the booth. Read RUBRIC.md, then open {clip.name}
with your file viewing tool and LISTEN. Do not run commands. It is a transition from "{a['title']}" into "{b['title']}":
type {w['type']}, {w['bars']} bars, the overlap runs from {rel0:.1f}s to {rel1:.1f}s in this clip.
The plan's reasoning was: "{w['why']}".
Score every rubric axis 1-10 honestly, apply the caps, name the single biggest flaw with its time in the clip,
and give the concrete fix. Do not be polite: a 7 means a working DJ would be fine with it, a 9 means people cheer."""
        log(f"critic listening to transition {w['index']} ...")
        c = agy(prompt, CRIT_SCHEMA, d, model=FAST)
        s = c["scores"]
        c["weighted"] = round(sum(WEIGHTS[k] * s.get(k, c["overall"]) for k in WEIGHTS), 2)
        c["index"] = w["index"]
        out.append(c)
    return out


# ---------------------------------------------------------------- the loop

def session(ids: list[str], brief: str, name: str, rounds=1, keep_order=True, on_event=lambda *_: None) -> dict:
    """plan -> verifiable rules -> render -> critic listens -> revise. Returns the best version."""
    from concurrent.futures import ThreadPoolExecutor
    with ThreadPoolExecutor(4) as ex:  # first listens in parallel; cached tracks return instantly
        list(ex.map(listen, ids))
    d = job_dir(name)
    feedback, best, history = "", None, []
    for r in range(rounds + 1):
        on_event("plan", r)
        p = plan(ids, brief, d, feedback, keep_order)
        metas = render.load_meta([t["id"] for t in p["tracks"]])
        check = rules.check(p, metas)
        log(f"round {r}: rules score {check['score']}", [v["message"] for v in check["violations"]])
        on_event("rules", check)
        if any(v["hard"] for v in check["violations"]):
            feedback = ("\nYOUR PREVIOUS PLAN FAILED THESE HARD RULES, fix every one:\n" +
                        "\n".join(f"- {v['rule']}: {v['message']}" for v in check["violations"]) +
                        f"\nPrevious plan: {json.dumps(p)}")
            continue
        on_event("render", r)
        mix = render.render(json.loads(json.dumps(p)), f"{name}_v{r}")
        on_event("critique", r)
        crits = critique(mix, d)
        score = min(c["weighted"] for c in crits) if crits else 10
        v = {"round": r, "plan": p, "rules": check, "mix": mix, "critiques": crits, "score": score}
        history.append(v)
        log(f"round {r}: critic {[c['weighted'] for c in crits]} -> {[c['biggest_flaw'] for c in crits]}")
        if best is None or score > best["score"]:
            best = v
        if score >= 8 or r == rounds:
            break
        feedback = ("\nYou rendered that plan and listened back. Your critic said:\n" +
                    "\n".join(f"- transition {c['index']}: {c['weighted']}/10. Flaw: {c['biggest_flaw']}. Fix: {c['fix']}" for c in crits) +
                    f"\nRules notes: {[x['message'] for x in check['violations']]}\nPrevious plan: {json.dumps(p)}\n"
                    "Revise the plan to fix these. Keep what worked.")
    if best is None:
        raise RuntimeError("no plan passed the hard rules")
    result = {"best": best, "history": [{k: h[k] for k in ("round", "score")} for h in history]}
    (d / "result.json").write_text(json.dumps(result, indent=1))
    on_event("done", best)
    return result


if __name__ == "__main__":
    import sys
    ids, brief = sys.argv[1].split(","), sys.argv[2]
    res = session(ids, brief, sys.argv[3] if len(sys.argv) > 3 else "cli")
    b = res["best"]
    print(json.dumps({"story": b["plan"]["story"], "file": b["mix"]["file"], "score": b["score"],
                      "transitions": b["plan"]["transitions"], "critiques": b["critiques"], "history": res["history"]}, indent=1))
