# MOTH: an AI DJ that listens

Takes two records and performs them like a DJ: Demucs stems, Beat This! beat grids, Whisper lyrics, Gemini (via `agy`) as planner and critic, a stem sequencer and mixing console in `dj/`, and a Vue deck UI in `web/` built on [dither-ui](https://dither-ui.com).

Bring your own audio: put files in `music/` (not tracked).

```
python -m venv .venv && .venv/Scripts/pip install -r requirements.txt   # see dj/ imports
cd web && npm i && npm run build
.venv/Scripts/python -m uvicorn server:app --app-dir dj --port 8077
```

See `HANDOFF.md` for the current state and next steps.
