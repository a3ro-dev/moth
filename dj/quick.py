"""Instant mix: brute-force search over phrase-aligned plans, scored by rules.check (the verifiable rewards).
No LLM, runs in milliseconds; MOTH's listened-and-revised plan replaces it when ready."""
import json

import render
import rules


def candidates(m, lo, hi):
    starts = {s["start_bar"] for s in m.get("sections", []) + m.get("ears", {}).get("sections", [])}
    return sorted({b for b in range(0, m["n_bars"]) if lo <= b / max(1, m["n_bars"]) <= hi and (b % 8 == 0 or b in starts)})


def pair(A, B, used_types, a_from=0.0):
    ratio = A["bpm"] / B["bpm"]
    gap = min(abs(ratio * k - 1) for k in (0.5, 1, 2))
    steady = min(A["grid_confidence"], B["grid_confidence"]) >= 0.8
    types = [("bass_swap", 16), ("eq_swap", 16), ("blend", 32), ("bass_swap", 8)] if gap <= 0.06 and steady else []
    types += [("echo_out", 2), ("cut", 0)]
    hint_in = {c["bar"] for c in B.get("ears", {}).get("mix_in", [])}
    hint_out = {c["bar"] for c in A.get("ears", {}).get("mix_out", [])}
    best = None
    for kind, n in types:
        for s in candidates(A, max(a_from, 0.45), 0.97):
            for cue in candidates(B, 0, 0.5):
                tr = {"start_bar": s, "bars": n, "type": kind}
                res = rules.check({"tracks": [{"id": A["id"]}, {"id": B["id"], "cue_in_bar": cue}], "transitions": [tr]}, [A, B])
                if res["score"] == 0:
                    continue
                # taste priors on top of the rules: use the ears' cue points, prefer longer beatmatched mixes,
                # don't repeat the last transition type, leave A late but not at the death
                score = res["score"] + 6 * (s in hint_out) + 6 * (cue in hint_in) + (4 if kind in render.BEATMATCHED else 0)
                score -= 5 * (used_types[-1:] == [kind]) + 10 * abs(s / A["n_bars"] - 0.8)
                if best is None or score > best[0]:
                    best = (score, tr, cue)
    if best is None:  # nothing passes: hard cut at the last phrase, the honest fallback
        return {"start_bar": A["n_bars"] // 8 * 8 - 8, "bars": 0, "type": "cut", "why": "no clean overlap exists, cut on the one"}, 0
    _, tr, cue = best
    tr["why"] = f"{tr['type'].replace('_', ' ')} over {tr['bars']} bars, out of bar {tr['start_bar']} into bar {cue} (rule search)"
    return tr, cue


def plan(ids: list[str]) -> dict:
    metas = render.load_meta(ids)
    tracks, trans, used = [{"id": ids[0], "cue_in_bar": 0}], [], []
    for A, B in zip(metas, metas[1:]):
        tr, cue = pair(A, B, used, a_from=tracks[-1]["cue_in_bar"] / A["n_bars"])
        trans.append(tr)
        used.append(tr["type"])
        tracks.append({"id": B["id"], "cue_in_bar": cue})
    p = {"story": "quick take while I listen properly.", "tracks": tracks, "transitions": trans}
    p["rules"] = rules.check(p, metas)
    return p


if __name__ == "__main__":
    import sys
    import time
    t = time.time()
    p = plan(sys.argv[1].split(","))
    print(f"planned in {time.time() - t:.2f}s", json.dumps(p, indent=1))
