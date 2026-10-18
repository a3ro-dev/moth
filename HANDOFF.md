# Handoff: MOTH, an AI DJ that listens (v2, 2026-10-17 late)

Read this first, then the code. The previous handoff's vision and constraints still hold:
- `agy` only (Gemini 3.8 Flash), no API key, no local LLMs.
- Non-LLM NNs are welcome. The user said "use 5 NNs, I don't mind, just get the job done".
- GPU: RTX 4050, 6 GB.
- Speed matters.
- Audio comes from user-owned files only.

## What the user wants (in their words, distilled)
- Viral-reel *performance* DJing, not crossfades. But **don't copy reels 1:1**: use the references (`refs/`) for principles and MOTH's own creativity.
- **Listenable first.** Their complaints, in order:
  1. "ew / slop": fixed, mostly engine bugs.
  2. "jerky": improved with seams.
  3. Now **"oil and water"**: the two records don't sound like one mix.
- They want a pro-grade deck, much more data fed to the models, and a **continuous learning / RLVR loop**.
- Best take so far: `saopaulo_tokyodrift_v2`, rated 👍 ("best so far, still oil-and-water + jerky at swaps"). Golmaal × Bananza rated 👎.
- Style: lowercase Hinglish, impatient. Keep them updated. Lean agents.

## NN stack
| Model | Role |
|---|---|
| Beat This! (`small0`) | Beat grid |
| Demucs **htdemucs_ft** | Stems. Cached in `data/stems_htdemucs_ft/`, ~40 s/track on GPU |
| Whisper **large-v3-turbo** (openai-whisper, `--no-deps`) | Word-timed lyrics on the vocal stem |
| Gemini via agy | Ears, planner, critic |

## What changed this session (all in `dj/`)
- **stems.py**
  - Uses htdemucs_ft; the profile cache is versioned by `stems_model`.
  - Vocal phrases are found at half-beat resolution: above -10 dB re p95, single half-beat gaps bridged. Silence gates fail on wall-to-wall vocals.
  - Phrase bars are now exact; rounding them made Gemini emit off-grid `at` values.
- **routine.py** (the sequencer)
  - Stretches only the used source window (68 s → 8 s).
  - Pad-choke chops.
  - `play_seams`:
    - Seamless continuation when the same deck and stem continue at the next src bar.
    - 5 ms declick on fresh entries.
    - Leaving stems ring out through a rising high-pass (`TAILS`).
  - Renders into **per-deck vox/beat buses** and passes them to `mixer.py`.
  - **Closed-loop grid lock:** measures each deck's offset from the master grid in the mix and cancels it (14.5 ms flam → 0).
  - New rules:
    - Hard: both decks pitch-shifted; a stem doubled at two src positions (DUP); drums/bass entering off a 4-bar line (R1, now hard).
    - FX budget: more than one FX move is flagged.
    - Length: 35–75 s.
- **render.py**: `master()`, which does LUFS normalize (-10) plus a 5 ms lookahead brickwall limiter. It replaced a tanh soft clip that was distorting everything (mix peaks hit 1.73).
- **mixer.py (new, "the console")**
  - Vocal HPF.
  - Vocal-over-foreign-beat level match to the vocal's native ratio.
  - Sidechained 1–5 kHz carve of the foreign beat under the vocal.
  - Shared room reverb send.
  - Glue compressor.
  - All knobs are in `KNOBS`.
- **measure.py (new, verifiable rewards)**: `sync_ms`, `grid_ms`, `vox_clarity_db`, `seam_db` (only at swap points, gaps excluded), `flow_db`, and `reward()` 0–1. The onset detector is custom with no lookahead; librosa's fired ~20 ms early.
- **lyrics.py (new)**
  - Whisper on the vocal stem with word timestamps mapped to bars.
  - `ground_hooks` moves Gemini's hook `src_bar` to where the words are actually sung, using a character (sound-alike) match. It only moves on a confident match (≥ 0.6), otherwise flags `grounded: 0`.
  - Per-chunk language detection with one pass per language (max 2), keeping the more confident segment. Rerun result:
    - It detected en+pt for São Paulo and en+ja for Tokyo Drift.
    - **Tokyo "Fast and furious" is still ungrounded.** Whisper hears it as "Fast and Play-O" at bar 17.58, so the hook keeps Gemini's wrong 13.38 (flagged `grounded: 0`). The planner does see the 17.58 line in `lyrics_exact`.
    - **"Bota na boca" moved 15.88 → 95.6.** That's suspicious: the intro chant may not be transcribed at all. Check this by ear or with forced alignment before trusting it.
    - Bug to fix: when `src_bar_heard` is None, `guess` falls back to 0.
    - This all strengthens next step 3 (forced alignment).
- **learn.py (new, the learning loop)**
  - `data/takes.jsonl` logs every take: plan, metrics, rules, critic, knobs, flaw/fix, and the user rating.
  - `total()`: rating > critic > measured > rules.
  - `lessons(ids)`: QenloDB in-memory vector search over pair vectors → the best past takes on similar pairs, written to the job as `lessons.json` for the planner.
  - `knobs()`: CEM-style mean of the elite takes' console knobs plus exploration noise.
- **perform.py**
  - Session flow: stems → listen → **lyrics** → plan (reads decks.json with `lyrics_exact` plus lessons.json) → snap `at` to 1/16 → check → render with `learn.knobs()` → critic (gets the measured metrics plus `ref_*.mp3`) → `learn.log_take`.
  - Prompts are rewritten: own idea, listenable, few moves, at most 1 FX, pitch-shift at most one deck.
- **brain.py**: removed `--effort`. agy now bakes the tier into the model name, and `--effort` with a tiered model errors.
- **server.py + web**: `POST /api/rate` plus ▲ LOVE / ▼ NAH buttons with a note prompt, feeding `learn.rate`.
- **skills/dj-craft/ROUTINES.md**: rewritten as principles: one song not two, famous moments only, restraint, surprise from the pairing.

## Numbers (same v2 plan, `saopaulo_tokyodrift_v2_raw` vs `_v2_console`)
- `grid_ms`: A -8.7 / B +5.8 → 0 / 0.
- Reward: 0.577 → 0.676.
- `vox_clarity_db`: about 3.9 either way.
- `seam_db` mean: ~12 dB. This is still high. Some of it is musical (entries); split "jerk" from "drop" before trusting it.
- `glue_gr_db` is only 0.3: the glue threshold at p75 barely bites. Try p50.

## Next steps (in order)
1. Check the lyrics rerun. Then run a fresh session:
   `cd dj && PYTHONIOENCODING=utf-8 ../.venv/Scripts/python perform.py 4ec26855b0a1,0e616b5878a5 "São Paulo x Tokyo Drift. make it something people replay: listenable first, your own idea, party energy" saopaulo_tokyodrift2`
   Expect ~15 min. Gemini -high planning is ~5–6 min per attempt, and a hard-rule bounce costs a full replan.
2. **Oil and water is still the #1 complaint.** Ideas not done yet:
   - Spectral matching: an EQ curve to match the foreign beat's tonal balance to the vocal's native beat (long-term average spectrum ratio, smoothed).
   - Bass-swap crossfades at drum handoffs (a 1-bar EQ swap instead of a cut).
   - Key-aware harmonic carve when 'other' stems from both decks overlap.
   - Measure a "timbre mismatch" metric (LTAS distance between vocal-native and vocal-foreign beds) and add it to `reward()`.
3. **Forced alignment beats Whisper** for lyrics: fetch the real lyrics (LRCLIB synced lyrics) and align them to the vocal stem with wav2vec2/MMS, WhisperX-style. Keep Whisper as the fallback.
4. **Speed:**
   - Reuse the agy conversation for revisions.
   - Auto-repair trivial hard violations (grid snaps, overlaps) instead of replanning.
   - Precompute stems, lyrics and listening on upload (`/api/upload`).
5. Audio embedding NN (CLAP or MERT) for the pair vector in `learn.pair_vec` and `/api/similar`, instead of the handcrafted timbre vector.
6. The UI should not present TAKE OVER (the crossfade engine) as the main path. The user clicked it and heard an 8-minute stitch.

## Gotchas
- Two background runs writing the same log file confused me. Give each run its own log.
- Killing perform runs on Windows: `TaskStop` the background task, or use PowerShell `Get-CimInstance Win32_Process` filtered on CommandLine. `ps`/`kill` and `wmic` don't work.
- `python -` without input hangs (the Windows Store alias). Always use `.venv/Scripts/python`.
- The folder is NOT a git repo yet, so no commits were made. The user prefers small atomic commits once it is one.
- This session's folder is an app scratch workspace: offer to move it to a real folder (e.g. `D:\moth`).
