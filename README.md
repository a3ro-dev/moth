# moth

an ai dj that listens before it plays.

give it two records and a vibe. it pulls them apart into stems, finds the beat grid, reads the lyrics off the vocal, then plans a short performance: a vocal from one song riding the drums of the other, chops, swaps, one fx move at most. it renders the mix, listens back to its own work, and revises. the goal is a mix you'd replay, not a crossfade.

it's early. the best take so far was rated "best so far, still oil-and-water and jerky at swaps". that's the honest state, and the main thing i'm working on (see below).

## how it works

```
two tracks + a brief
  -> demucs htdemucs_ft       stems (vocals / drums / bass / other)
  -> beat this!               beat grid
  -> whisper large-v3-turbo   word-timed lyrics on the vocal stem, mapped to bars
  -> gemini via agy           listens, plans the routine, then critiques the render
  -> rules.py                 hard/soft checks on the plan (grid, doubled stems, fx budget, length)
  -> routine.py               stem sequencer: pad chops, seamless continuations, grid lock
  -> mixer.py                 the console: vocal hpf, sidechain carve, shared reverb, glue comp
  -> render.py                lufs normalize + lookahead limiter
  -> measure.py               verifiable scores (sync, grid, vocal clarity, seam, flow)
  -> learn.py                 logs every take, steers the next plan and console knobs
```

a few decisions worth knowing:

- **llm only through `agy`**, no api key, no local llms. other models are plain old nets (beat this!, demucs, whisper).
- **the plan is checked before it's rendered.** gemini's timestamps are often a bit off, so `at` values get snapped to 1/16 and hard-rule violations bounce the plan back.
- **hooks are grounded in the actual lyrics.** if gemini says a line is at bar 13 and whisper hears it at bar 17, the plan moves, but only on a confident match. otherwise it's flagged `grounded: 0`.
- **the mix is measured, not just judged.** `measure.py` gives a 0 to 1 reward from numbers (grid offset in ms, vocal clarity in dB, seam loudness jumps). the onset detector is custom because librosa's fired ~20 ms early.
- **it learns from takes.** `data/takes.jsonl` stores plan, metrics, critic score and your rating. past takes on similar pairs feed the planner, and the console knobs drift toward what scored well.

## run it

needs python with a cuda gpu (built on an rtx 4050, 6 gb), node, and `agy` on your path. there's no requirements file yet, so install what `dj/` imports: `torch`, `demucs`, `beat_this`, `openai-whisper`, `librosa`, `fastapi`, `uvicorn`.

```bash
python -m venv .venv
cd web && npm i && npm run build && cd ..
.venv/Scripts/python -m uvicorn server:app --app-dir dj --port 8077
```

open `localhost:8077`, pick two records, type a vibe, hit perform. a first take shows up on the decks as soon as it's rendered (a few minutes), while the critic and the revision keep going in the background.

or from the command line, one session:

```bash
cd dj && python perform.py <id_a>,<id_b> "your brief" take_name
```

expect ~15 min a session. most of that is gemini planning.

## bring your own audio

`music/`, `data/` and `refs/` are gitignored. drop your own files in `music/` (or upload through the ui). nothing copyrighted lives in this repo.

## layout

| path | what |
|---|---|
| `dj/` | the engine: analysis, stems, lyrics, planner, sequencer, console, metrics, server |
| `web/` | vue deck ui, built on [dither-ui](https://dither-ui.com) (vendored in `web/src/dither-kit`, mit) |
| `skills/dj-craft/` | the craft notes the planner reads: principles, rubric, routines |

## what's not working yet

- **oil and water.** the two records still don't always sound like one mix. next: match the foreign beat's spectrum to the vocal's native one, bass-swap at drum handoffs, add a timbre-mismatch score to the reward.
- **lyrics are whisper-only.** it mishears sung hooks ("fast and furious" came out as "fast and play-o"). forced alignment against real synced lyrics should be better.
- **slow.** gemini planning is most of a session, and a hard-rule bounce costs a full replan.
- windows-tested only.
