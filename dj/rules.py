"""Verifiable rewards: deterministic checks from skills/dj-craft/SKILL.md section 9.

check(plan, meta) -> {"score": 0-100, "violations": [...]} where hard violations zero the score.
Rule ids match the skill file so the planner can look up the reasoning.
"""

BEATMATCHED = {"blend", "bass_swap", "eq_swap", "filter"}
LENGTHS = {0, 1, 2, 4, 8, 12, 16, 24, 32, 48, 64}


def camelot_relation(a: str, b: str) -> str:
    na, la, nb, lb = int(a[:-1]), a[-1], int(b[:-1]), b[-1]
    step = (nb - na) % 12
    if la == lb:
        return {0: "same", 1: "+1", 11: "-1", 2: "+2", 7: "+7"}.get(step, "clash")
    if step == 0:
        return "relative"
    return "diagonal" if step in (1, 11) else "clash"


KEY_SCORE = {"same": 1, "+1": 1, "-1": 1, "relative": 1, "diagonal": .7, "+2": .8, "+7": .6, "clash": 0}


def bar_sec(m):
    return 4 * m["beat_period"]


def phrase_ok(m, bar):
    starts = {s["start_bar"] for s in m.get("sections", []) + m.get("ears", {}).get("sections", [])}
    return bar % 8 == 0 or bar in starts or (bar % 4 == 0 and bar in {s + 4 for s in starts})


def vocal_bars(m):
    return {b for a, z in m.get("ears", {}).get("vocal_bars", []) for b in range(a, z)}


def check(plan: dict, meta: list[dict]) -> dict:
    v = []  # (rule, hard, weight, score 0..1, message)
    tracks, trans = plan["tracks"], plan["transitions"]

    ids = [t["id"] for t in tracks]
    if len(set(ids)) != len(ids):
        v.append(("R36", True, 1, 0, "a track is played twice"))
    if len(trans) != len(tracks) - 1:
        v.append(("SCHEMA", True, 1, 0, f"{len(tracks)} tracks need {len(tracks) - 1} transitions, got {len(trans)}"))
        return summarize(v)

    played = []
    for i, tr in enumerate(trans):
        A, B = meta[i], meta[i + 1]
        cue = tracks[i + 1].get("cue_in_bar", 0)
        s, n, kind = tr["start_bar"], tr["bars"], tr["type"]
        tag = f"T{i} {A['title'][:18]} -> {B['title'][:18]}"

        if kind not in BEATMATCHED | {"echo_out", "cut"}:
            v.append(("SCHEMA", True, 1, 0, f"{tag}: unknown type {kind}"))
            continue
        if s + n > A["n_bars"] or cue + n > B["n_bars"]:
            v.append(("SCHEMA", True, 1, 0, f"{tag}: transition runs past the end of a track"))
        if not phrase_ok(A, s):
            v.append(("R1", True, 1, 0, f"{tag}: A exits at bar {s}, not a phrase boundary (mod 8 or section start)"))
        if not phrase_ok(B, cue):
            v.append(("R1", True, 1, 0, f"{tag}: B enters at bar {cue}, not a phrase boundary"))
        if n not in LENGTHS:
            v.append(("R4", True, 1, 0, f"{tag}: {n} bars is not a quantized length"))

        ratio = A["bpm"] / B["bpm"]
        octave = min((abs(ratio * k - 1), k) for k in (0.5, 1, 2))[1]
        gap = abs(ratio * octave - 1)
        if kind in BEATMATCHED:
            if gap > 0.08:
                v.append(("R25", True, 1, 0, f"{tag}: tempos differ {gap:.0%}; beatmatched {kind} will sound warped, use cut/echo_out"))
            elif n > 2 and min(A.get("grid_confidence", 1), B.get("grid_confidence", 1)) < 0.8:
                v.append(("R26", True, 1, 0, f"{tag}: beat grid too unsteady (confidence < 0.8) for a {n}-bar beatmatched overlap"))
            elif gap > 0.06:
                v.append(("R22", False, 2, 0.5, f"{tag}: {gap:.1%} stretch is audible on B"))
            if octave != 1:
                v.append(("R22", False, 1, 0.6, f"{tag}: half/double-time relation, check groove"))

            overlap = n
            vb_a = {b - s for b in vocal_bars(A) if s <= b < s + n}
            vb_b = {b - cue for b in vocal_bars(B) if cue <= b < cue + n}
            clash = len(vb_a & vb_b)
            if clash > 2:
                v.append(("R16", True, 1, 0, f"{tag}: vocals overlap for {clash} bars"))
            elif clash:
                v.append(("R16", False, 3, 0.5, f"{tag}: vocals overlap for {clash} bar(s)"))
            rel = camelot_relation(A["camelot"], B["camelot"])
            if overlap >= 4 and KEY_SCORE[rel] < 1:
                if rel in ("+2", "+7") and not tr.get("energy_boost"):
                    v.append(("R18", False, 3, 0.3, f"{tag}: {A['camelot']}->{B['camelot']} ({rel}) only works as a flagged energy boost"))
                else:
                    v.append(("R18", False, 3, KEY_SCORE[rel], f"{tag}: {A['camelot']}->{B['camelot']} is a {rel} over {overlap} bars of overlap"))
            # R7: B should take over on a section with real energy
            sw = cue + n // 2
            e = B["bar_energy"][sw:sw + 4] if sw < len(B["bar_energy"]) else []
            emax = max((sum(r) / 3 for r in B["bar_energy"]), default=1)
            if e and sum(sum(r) / 3 for r in e) / len(e) < 0.4 * emax:
                v.append(("R7", False, 2, 0.4, f"{tag}: B is weak at the switch (bar {sw}), takeover won't land"))
        played.append(kind)

    # R27 variety
    for i in range(len(played) - 2):
        if played[i] == played[i + 1] == played[i + 2]:
            v.append(("R27", False, 2, 0.3, f"{played[i]} used 3 times in a row from T{i}: template smell"))
    # R9 let tracks breathe: solo time per track
    for i, m in enumerate(meta):
        cue = tracks[i].get("cue_in_bar", 0)
        start = cue + (trans[i - 1]["bars"] if i else 0)
        end = trans[i]["start_bar"] if i < len(trans) else m["n_bars"]
        solo = (end - start) * bar_sec(m)
        if solo < 30:
            v.append(("R9", False, 2, max(0, solo / 30), f"{m['title'][:24]} only plays {solo:.0f}s solo; let it breathe"))
    return summarize(v)


def summarize(v):
    hard = [x for x in v if x[1]]
    soft = [x for x in v if not x[1]]
    # soft rules not listed scored 1.0; weight base of 10 keeps one soft miss from tanking the score
    total_w = 10 + sum(w for _, _, w, _, _ in soft)
    soft_score = (10 + sum(w * s for _, _, w, s, _ in soft)) / total_w
    return {"score": 0 if hard else round(100 * soft_score, 1),
            "violations": [{"rule": r, "hard": h, "message": msg} for r, h, _, _, msg in v]}


if __name__ == "__main__":
    assert camelot_relation("8A", "9A") == "+1" and camelot_relation("8A", "8B") == "relative"
    assert camelot_relation("12A", "1A") == "+1" and camelot_relation("8A", "3B") == "clash"
    assert camelot_relation("8B", "10B") == "+2" and camelot_relation("8A", "9B") == "diagonal"
    m = {"title": "x", "bpm": 120, "beat_period": .5, "n_bars": 100, "camelot": "8A", "sections": [],
         "bar_energy": [[1, 1, 1]] * 100}
    ok = check({"tracks": [{"id": "a"}, {"id": "b", "cue_in_bar": 0}],
                "transitions": [{"start_bar": 64, "bars": 16, "type": "bass_swap"}]}, [m, dict(m, title="y")])
    assert ok["score"] == 100, ok
    bad = check({"tracks": [{"id": "a"}, {"id": "b", "cue_in_bar": 3}],
                 "transitions": [{"start_bar": 61, "bars": 10, "type": "blend"}]}, [m, dict(m, bpm=135, title="y")])
    assert bad["score"] == 0 and {x["rule"] for x in bad["violations"]} >= {"R1", "R4", "R25"}, bad
    print("rules ok")
