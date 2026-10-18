"""MOTH backend. Run: .venv/Scripts/python -m uvicorn server:app --app-dir dj --port 8077"""
import json
import shutil
import threading
import time
import uuid
from pathlib import Path

from fastapi import FastAPI, HTTPException, UploadFile
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

import analyze
import brain
import learn
import perform
import quick
import render
from concurrent.futures import ThreadPoolExecutor

ROOT = Path(__file__).resolve().parent.parent
MUSIC = ROOT / "music"
AUDIO = {".mp3", ".m4a", ".wav", ".flac", ".ogg", ".aac"}
MUSIC.mkdir(exist_ok=True)
app = FastAPI()
ears = ThreadPoolExecutor(3)  # Gemini listens run remotely, so they don't take the heavy-job lock
jobs: dict[str, dict] = {}
lock = threading.Lock()  # ponytail: one heavy job at a time (laptop-friendly); a queue if this ever serves many users


def card(m: dict) -> dict:
    keep = ("id", "title", "bpm", "key", "camelot", "duration", "lufs", "grid_confidence", "n_bars", "waveform", "downbeats")
    c = {k: m.get(k) for k in keep}
    c["downbeats"] = c["downbeats"][::8] if c["downbeats"] else []
    if "ears" in m:
        c["ears"] = {k: m["ears"][k] for k in ("genre", "language", "mood", "energy", "vibe", "warnings")}
        c["sections"] = [{k: s.get(k) for k in ("start_s", "end_s", "label", "vocals")} for s in m["ears"]["sections"]]
    return c


def library():
    metas = {m["path"]: m for m in (json.loads(p.read_text()) for p in analyze.CACHE.glob("*.json"))}
    files = [p for p in MUSIC.iterdir() if p.suffix.lower() in AUDIO]
    return metas, files


@app.get("/api/library")
def get_library(q: str = ""):
    metas, files = library()
    out = []
    for f in files:
        m = metas.get(str(f.resolve()))
        item = card(m) if m else {"id": None, "title": f.stem, "pending": True}
        item["file"] = f.name
        if q.lower() in item["title"].lower() or q.lower() in json.dumps(item.get("ears", {})).lower():
            out.append(item)
    return out


@app.post("/api/upload")
async def upload(files: list[UploadFile]):
    for f in files:
        name = Path(f.filename).name
        if Path(name).suffix.lower() not in AUDIO:
            raise HTTPException(400, f"{name}: not an audio file")
        with open(MUSIC / name, "wb") as out:
            shutil.copyfileobj(f.file, out)
    names = [Path(f.filename).name for f in files]

    def run(job):
        for n in names:  # dissect now, then MOTH listens in the background so MIX never waits on it
            ears.submit(brain.listen, analyze.analyze(MUSIC / n)["id"])
    return start(run, "analyze")


def start(fn, kind, key=None):
    """key: identical requests (a double click, a reload) join the live job instead of queueing a duplicate."""
    for j in jobs.values():
        if key and j.get("key") == key and j["status"] in ("queued", "running"):
            return j
    jid = uuid.uuid4().hex[:8]
    job = jobs[jid] = {"id": jid, "kind": kind, "key": key, "status": "queued", "events": [], "result": None, "error": None}

    def run():
        with lock:
            job["status"] = "running"
            try:
                job["result"] = fn(job)
                job["status"] = "done"
            except Exception as e:  # surfaced to the UI, not swallowed
                job["status"], job["error"] = "error", f"{type(e).__name__}: {e}"
    threading.Thread(target=run, daemon=True).start()
    return job


@app.post("/api/analyze/{filename}")
def analyze_file(filename: str):
    path = MUSIC / Path(filename).name
    if not path.exists():
        raise HTTPException(404)
    def run(job):
        ears.submit(brain.listen, analyze.analyze(path)["id"])
    return start(run, "analyze")


class MixReq(BaseModel):
    ids: list[str]
    brief: str = ""
    takeover: bool = False
    mode: str = "routine"  # routine = stems + moves performance; set = long blended mix


class RateReq(BaseModel):
    name: str
    rating: int  # +1 / -1
    note: str = ""


@app.post("/api/rate")
def rate(req: RateReq):
    """The user's verdict: the strongest reward in the learning loop."""
    learn.rate(Path(req.name).stem, 1 if req.rating > 0 else -1, req.note[:500])
    return {"ok": True}


@app.post("/api/mix")
def mix(req: MixReq):
    if len(req.ids) < 2:
        raise HTTPException(400, "need at least two tracks")

    def ev_for(job):
        def ev(kind, data):
            msg = {"plan": "reading the records, writing a plan", "rules": None, "render": "on the decks, rendering",
                   "critique": "listening back with fresh ears", "done": "done",
                   "stems": "splitting both records into vocals / drums / bass / melody (GPU)",
                   "listen": "listening for the hooks"}.get(kind)
            if kind == "rules":
                msg = f"rule check {data['score']}/100" + (f" - {data['violations'][0]['message']}" if data["violations"] else "")
            if kind == "preview":
                job["preview"] = data
                msg = f"take {data['round'] + 1} is on the decks: press play. i'm listening back and revising"
            job["events"].append({"t": time.time(), "kind": kind, "msg": msg})
        return ev

    if req.mode == "routine" and not req.takeover:
        return start(lambda job: pack(perform.session(req.ids[:2], req.brief or "perform these like a viral DJ clip",
                                                      f"routine_{job['id']}", on_event=ev_for(job))), "routine",
                     key=("routine", *req.ids[:2], req.brief))

    def run(job):
        def ev(kind, data):
            msg = {"plan": "reading the records, writing a plan", "rules": None, "render": "on the decks, rendering",
                   "critique": "listening back with fresh ears", "done": "done"}.get(kind)
            if kind == "rules":
                msg = f"rule check {data['score']}/100" + (f" - {data['violations'][0]['message']}" if data["violations"] else "")
            job["events"].append({"t": time.time(), "kind": kind, "msg": msg})
        # instant take: rule-searched plan, rendered in seconds, playable while MOTH listens properly
        qp = quick.plan(req.ids)
        job["events"].append({"t": time.time(), "kind": "quick", "msg": "quick take on the decks while i listen properly"})
        qm = render.render({k: qp[k] for k in ("tracks", "transitions")}, f"quick_{job['id']}")
        job["preview"] = {"story": qp["story"], "plan": qp, "mix": qm, "critiques": [], "score": None, "rules": qp["rules"], "history": []}
        unheard = [json.loads((analyze.CACHE / f"{i}.json").read_text()) for i in req.ids]
        for m in unheard:
            if "ears" not in m:
                job["events"].append({"t": time.time(), "kind": "listen", "msg": "listening to " + m["title"]})
        res = brain.session(req.ids, req.brief or "mix these like a real DJ", f"mix_{job['id']}",
                            keep_order=not req.takeover, on_event=ev)
        return pack(res)
    return start(run, "mix")


@app.get("/api/active")
def active():
    """The live job, so a reloaded page re-attaches instead of losing it."""
    live = [j for j in jobs.values() if j["status"] in ("queued", "running")]
    return live[-1] if live else None


@app.get("/api/jobs/{jid}")
def job(jid: str):
    if jid not in jobs:
        raise HTTPException(404)
    return jobs[jid]


@app.get("/api/similar/{tid}")
def similar(tid: str, k: int = 5):
    """QenloDB: nearest records by timbre/groove/key vector, i.e. 'what could come next'."""
    from qenlo._collection import Collection, Record
    metas = [json.loads(p.read_text()) for p in analyze.CACHE.glob("*.json")]
    ids = {i: m for i, m in enumerate(metas)}
    with Collection.memory(dimension=len(metas[0]["vector"])) as db:
        db.add_batch(Record(id=i, user_id=0, timestamp=0, vector=m["vector"]) for i, m in ids.items())
        q = next(m for m in metas if m["id"] == tid)
        res = db.search(query=q["vector"], k=k + 1)
    return [{"id": ids[r.id]["id"], "title": ids[r.id]["title"], "score": round(float(r.score), 3)}
            for r in res.results if ids[r.id]["id"] != tid]


def pack(res: dict) -> dict:
    b = res["best"]
    mix = b["mix"]
    if "waveform" not in mix:  # mixes rendered before waveforms existed
        y = analyze.load(render.OUT / mix["file"])
        mix["waveform"] = analyze.waveform(analyze.band_energy(y, 512), 2400)
    return {"story": b["plan"]["story"], "plan": b["plan"], "mix": mix, "critiques": b["critiques"],
            "score": b["score"], "rules": b["rules"], "history": res["history"]}


@app.get("/api/latest")
def latest():
    done = sorted(brain.JOBS.glob("*/result.json"), key=lambda p: p.stat().st_mtime)
    return pack(json.loads(done[-1].read_text())) if done else None


@app.get("/api/mixes")
def mixes():
    return sorted((json.loads(p.read_text()) | {"plan": None} for p in render.OUT.glob("*.json")),
                  key=lambda m: -Path(render.OUT / m["file"]).stat().st_mtime)


@app.get("/audio/mix/{name}")
def mix_audio(name: str):
    p = render.OUT / Path(name).name
    if not p.exists():
        raise HTTPException(404)
    return FileResponse(p)


@app.get("/audio/track/{filename}")
def track_audio(filename: str):
    p = MUSIC / Path(filename).name
    if not p.exists():
        raise HTTPException(404)
    return FileResponse(p)


app.mount("/", StaticFiles(directory=ROOT / "web" / "dist", html=True), name="web")  # cd web && npm run build
