"""MOTH's memory and learning loop (RLVR without touching Gemini's weights).

Every take is logged to data/takes.jsonl with its verifiable rewards:
  measured (measure.reward: sync, grid, clarity, seams, flow), rules (routine.check), critic (Gemini listening),
  and the user's rating when given (it outranks everything else).
What learns from it:
  lessons(ids)  past takes of the most similar pairs (QenloDB vector search) -> the planner sees what scored and why
  knobs()       console settings, cross-entropy style: mean of the elite takes' knobs plus a little exploration
"""
import json
import time

import numpy as np

import analyze
import mixer

TAKES = analyze.CACHE.parent / "takes.jsonl"
SIGMA = {"carve_db": 1.0, "room_send_vox": 0.03, "room_send_beat": 0.01, "room_rt": 0.1, "glue_gr_db": 0.5, "spec_match_db": 1.5}
BOUNDS = {"carve_db": (0, 9), "room_send_vox": (0, 0.3), "room_send_beat": (0, 0.12), "room_rt": (0.3, 1.5), "glue_gr_db": (0, 4), "spec_match_db": (0, 9)}


def total(t):
    """One number per take. A human rating dominates; otherwise ears (critic) > measured > rules."""
    parts = [(0.45, (t.get("critic") or 0) / 10 if t.get("critic") is not None else None),
             (0.35, (t.get("metrics") or {}).get("reward")),
             (0.20, (t.get("rules") or 0) / 100 if t.get("rules") is not None else None)]
    have = [(w, v) for w, v in parts if v is not None]
    s = sum(w * v for w, v in have) / sum(w for w, _ in have) if have else 0.0
    if t.get("rating") is not None:  # +1 / -1 from the user
        s = 0.4 * s + 0.6 * (t["rating"] + 1) / 2
    return round(s, 3)


def takes():
    if not TAKES.exists():
        return []
    out = {}
    for line in TAKES.read_text(encoding="utf-8").splitlines():
        t = json.loads(line)
        out[t["name"]] = out.get(t["name"], {}) | t  # later lines (ratings) update earlier ones
    return list(out.values())


def log_take(name, ids, plan, metrics, rules, critic=None, knobs=None, **extra):
    t = {"name": name, "ids": list(ids), "time": time.time(), "plan": plan, "metrics": metrics, "rules": rules,
         "critic": critic, "knobs": knobs or dict(mixer.KNOBS)} | extra
    TAKES.parent.mkdir(parents=True, exist_ok=True)
    with TAKES.open("a", encoding="utf-8") as f:
        f.write(json.dumps(t) + "\n")


def rate(name, rating, note=""):
    with TAKES.open("a", encoding="utf-8") as f:
        f.write(json.dumps({"name": name, "rating": int(rating), "rating_note": note}) + "\n")


def pair_vec(ids):
    v = [np.array(json.loads((analyze.CACHE / f"{i}.json").read_text(encoding="utf-8"))["vector"], float) for i in ids]
    v = [x / (np.linalg.norm(x) + 1e-9) for x in v]
    return np.concatenate(sorted(v, key=lambda x: tuple(x[:3])))  # order-free: A x B == B x A


def lessons(ids, k=4):
    """The k best-scored past takes among the most similar pairs, as compact notes for the planner."""
    ts = [t for t in takes() if t.get("plan") and len(t.get("ids", [])) == 2]
    if not ts:
        return []
    from qenlo._collection import Collection, Record
    q = pair_vec(ids)
    with Collection.memory(dimension=len(q)) as db:
        db.add_batch(Record(id=i, user_id=0, timestamp=0, vector=pair_vec(t["ids"]).tolist()) for i, t in enumerate(ts))
        near = [ts[r.id] for r in db.search(query=q.tolist(), k=min(len(ts), 12)).results]
    near.sort(key=total, reverse=True)
    out = []
    for t in near[:k]:
        evs = sorted(t["plan"].get("events", []), key=lambda e: e["at"])
        out.append({"take": t["name"], "score": total(t), "user_rating": t.get("rating"), "user_note": t.get("rating_note"),
                    "critic_flaw": t.get("flaw"), "measured": {k: (t.get("metrics") or {}).get(k) for k in ("sync_ms", "vox_clarity_db", "seam_db")},
                    "idea": t["plan"].get("story"), "shape": [f"{e['at']} {e['move']} {e.get('deck', '')} {'+'.join(e.get('stems') or [])}" for e in evs][:24]})
    return out


def knobs(explore=True, elite=5, rng=np.random.default_rng()):
    """Console settings: mean of the elite takes' knobs (+ exploration noise), defaults until there is data."""
    ts = sorted([t for t in takes() if t.get("knobs") and (t.get("critic") is not None or t.get("rating") is not None)],
                key=total, reverse=True)[:elite]
    k = dict(mixer.KNOBS)
    if len(ts) >= 3:
        for key in SIGMA:
            k[key] = float(np.mean([t["knobs"].get(key, k[key]) for t in ts]))
    if explore:
        for key, s in SIGMA.items():
            k[key] = float(np.clip(k[key] + rng.normal(0, s), *BOUNDS[key]))
    return k


if __name__ == "__main__":
    for t in sorted(takes(), key=total, reverse=True)[:10]:
        print(f"{total(t):.3f}  {t['name']:36} critic={t.get('critic')} measured={(t.get('metrics') or {}).get('reward')} rating={t.get('rating')}")
