# Routines: performing two records, not stitching them

A routine is a short performance (45-120 s) where the DJ *plays* the records: splits them into parts,
teases, builds, drops, and calls back. This is what viral DJ clips are. A crossfade is not a routine.

You have four stems per record: `vocals`, `drums`, `bass`, `other` (melody, chords, instruments, FX).
You control each one, on a single master tempo, with these moves: play, loop, roll, chop, riser, impact,
gap, tape_stop, backspin, plus per-move filter sweeps (`lp_up` opens a muffled entry, `hp_up` thins an exit,
`lp_down` drowns a section, `hp_down` lets the bass back in), fades, gain and echo throws.

## The form: "oil and water"
The reel the user wants: two records that sound like they have NOTHING in common (a Bollywood banger and a
Brazilian funk track, a rap verse and a K-pop hook) and the DJ makes them lock so well the room starts vibing.
The joy is the "wait, how does that fit?!" moment. The engine of it:
1. **Establish** (4-8 bars): play record A so it is instantly recognisable: its most famous line, its own beat.
   The listener thinks "ok, this song".
2. **Tension** (optional, 1-2 bars): a loop, a filter, or a short `gap` right on the phrase line.
3. **The flip**: A's famous vocal keeps going, but now it sits on B's beat (B's drums+bass, maybe B's riff),
   key and tempo matched, landing on a downbeat. This is the moment. Give it 8+ clean bars so it sinks in.
4. **Payoff** (optional): answer with B's own hook over the same beat, or flip back, or chop A's word on B's groove.
5. **Out** on a line with an echo throw.
What makes the flip land: the vocal is on-key over the new beat (pitch-shift the VOCAL deck +/-1-2 if needed),
its phrase starts exactly where the new beat's phrase starts, and the new beat's energy is equal or higher.
Pick which record gives the vocal and which gives the beat by what will surprise most AND fit: the most famous
vocal over the most unexpected groove. That pairing choice is your creativity.

## Why the clips people love are listenable (principles, not templates)
Studied from real reels the user loves. Do NOT copy their structure; find what THESE two records want to do.
What those clips have in common:
- They sound like ONE song, not two. A single groove carries most of the clip, and the records meet where they
  genuinely agree (a shared rhythm, a line that answers another line, a riff that fits under a hook).
- The famous moments only. Nobody waits through verses; every second is a line people know.
- Restraint. Long clean stretches where the music just plays, then one or two moves that make you grin.
  A move earns its place by being musical (a word repeated because it's catchy, a swap because the lines
  answer each other), never because a routine "should have a build".
- Surprise comes from the pairing and the timing, not from effects.

Rules that keep it listenable:
- Hook in the first 2 seconds. No intros, no slow filter fades in.
- One beat swap (the flip), then the groove stays put. Swapping the beat every 8 bars is a medley, not a routine.
  Ping-ponging vocals of both records over one beat is NOT the flip; it reads as two songs taking turns.
- Swaps are hard cuts on the phrase line (`fade_in`/`fade_out` 0 or a few hundredths of a bar), not fades.
- Pads, not FX: chops of real words carry the energy. riser / impact / tape_stop / backspin are rare seasoning:
  0 or 1 in a whole clip. A `gap` (half a beat to 1 beat) right before a reveal is the one trick worth using.
- End on a line, or a chop of the tag, with an `echo` throw. Never a long fade.
- After the flip the vocal keeps flowing: go to the NEXT phrase (vocal_phrases), not back to a line already
  played. Replaying the same lyric within 16 bars sounds like a skip, and 1-2 bar vocal holes over a running
  beat sound like the record cut out. Repeat a word only as a deliberate chop.

## Mashup rules
- One lead vocal at a time. Acapella over instrumental = vocals from one deck, drums/bass/other from the other.
- One bassline at a time. When two decks play, at most one has `bass`.
- Keys: if both decks have melodic parts (vocals/other) playing together for more than 2 bars, they must be
  Camelot-compatible. Fix it with `semitones` (+/-1 or 2 on one deck, preferably the vocal deck). If they still
  clash, only layer drums/bass under the vocal, or chop instead of sustaining.
- Tempo: pick `master_bpm` between the two. Vocals tolerate about 15% stretch; full drums sound off past ~10%.
  For a big gap, stretch the vocal deck more than the drum deck, or use `tempo_mult` 0.5/2 for half/double time
  (e.g. a 70 BPM rap over a 140 beat).
- Use the `vocal_phrases` table: start a vocal `play` at a phrase start and end it at a phrase end, so no word
  gets chopped mid-syllable. Use `src` with beat fractions (x.25, x.5, x.75) to hit the exact pickup.

## Chops and rolls
- A chop is a **recognizable word or syllable**, 0.5-1 beat long, fired on a rhythm: e.g. hits [0, 0.5, 1, 1.5, 2, 3]
  for "gol-gol-gol-gol-GOL...MAAL". Put chops on the grid. Fire them where the beat breathes.
- A roll starts at 1 beat (or 2) and halves; it always ends on the drop downbeat.
- A loop of 1-2 beats under a filter is a classic build; a 4-bar loop extends a section you love.

## Taste: what separates a great routine from slop
- Every move has a reason you could say out loud ("tease the sax before the drop"). No move is decoration.
- At most 1 FX move (riser/impact/tape_stop/backspin) per clip. Let the songs do the work.
- Contrast is the point: rap into a singalong, sparse into dense, minor into major. But the bridge between them
  (shared tempo, a key that agrees, a rhythmic word) must be smooth.
- Surprise once. A routine with one unexpected, perfectly-placed moment beats one with ten tricks.
- Never leave dead air except an intentional gap. Never let two hooks fight. Never let the drop land off-grid.
- If it sounds like a medley, it's wrong. If a listener says "wait, how did those fit?", it's right.
