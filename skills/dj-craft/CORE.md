# DJ Craft — core (condensed from SKILL.md; full rules R1-R43 live there)

### 1.2 Principles of taste
1. **Serve the room, not your ego.** Writing on the opening DJ, Resident Advisor says warm-up DJs who use the slot to show off get the opposite of what they want. A great opener knows where the headliner will *start*, not where the headliner will be two hours in. For a planner, this means the target energy is set by the slot (opening, peak, closing, wedding, background), not by the "best" tracks in the library.
2. **Restraint is a skill.** Overusing effects shows up as a top beginner mistake in almost every guide surveyed. One DJ school puts it this way: if a track really sounded better with constant effects, the producer would have made it that way. DJ TechTools: if you touch the knobs every 30 seconds, stop.
3. **Let tracks breathe.** Each track tells a story, so let it play its part before mixing out, and don't cut a track off before it finishes its section (Digital DJ Tips, house mixing guide). If people are enjoying a song, don't rush into the next one (DJ TechTools, reading the floor).
4. **Tell a story with tension and release.** Verses, builds and dissonance create tension. Choruses, drops and resolution release it. A set that is all tension or all release loses the room. Contrast should exist inside tracks and across the set (Digital DJ Tips).
5. **Know when NOT to mix.** Not every pair of tracks wants a long blend:
   - Dense, melodic or vocal-heavy material often sounds best with a short overlap, a cut on the one, or an echo out.
   - If two tracks clash, a clean 1-beat cut is better than 32 bars of mud.
   - Sometimes the most musical move is to let a track play out its natural ending and start the next one on the downbeat. Digital DJ Tips calls this the "end-to-end".
6. **One track leads at any moment.** Digital DJ Tips calls it the "dominator": the track whose removal would make the mix sound weak. Losing track of which one is leading is a classic error.
7. **Think in chapters, not tracks.** Pan-Pot (Pioneer DJ blog) say one reaction to one track tells you very little, and a pattern across several tracks tells you much more. Plan in blocks of 3 to 5 tracks with a purpose (build, hold, reset, peak, breather).
8. **Don't over-plan.** Experienced DJs plan a few key mixes and leave room to adapt (DJ TechTools, "5 bad habits"). For an offline planner, this means avoiding a rigid, uniform template applied to every transition.


### 1.3 Great versus mediocre (summary)

| Mediocre | Great |
|---|---|
| Mixes as soon as the next track is beatmatched | Mixes when the *music* asks for it, at a structural boundary |
| Same transition every time, same length | Picks the transition to fit the pair and the moment |
| Plays all the bangers early | Saves weapons; peaks late and deliberately |
| Effects as decoration | Effects that complement what the producer already did |
| Trusts sync and key labels blindly | Listens: groove, timbre, vocals, low end |
| Two basslines and two vocals fighting | One bassline and one lead vocal at a time |
| Constant intensity | Peaks and valleys; breathers |

Sources: RA, "The esoteric art of the opening DJ" (https://ra.co/features/1095; repost https://jacksondeep.wordpress.com/the-esoteric-art-of-the-opening-dj/); Digital DJ Tips, "The Ultimate Guide To Mixing House Music" (https://www.digitaldjtips.com/the-ultimate-guide-to-mixing-house-music/); DJ TechTools, "5 Bad Habits That Experienced DJs Grow Out Of" (https://djtechtools.com/2018/05/07/5-bad-habits-that-experienced-djs-stop-doing/); DJ TechTools, "Reading A Dance Floor" (https://djtechtools.com/amp/2018/01/08/reading-dance-floor-important-dj-skill/); Pioneer DJ blog, "How to read a crowd" (https://blog.pioneerdj.com/djtips/how-to-read-a-crowd/); Club Ready DJ School, "7 Common Beginner DJ Mistakes" (https://www.clubreadydjschool.com/tribe-talk/getting-started/7-common-beginner-dj-mistakes); Kim, Yang & Nam, DAFx 2022 (https://mac.kaist.ac.kr/pubs/KimYangNam-dafx2022.pdf); Brewster & Broughton, *How to DJ Right* (Grove Press, 2003; publisher page https://groveatlantic.com/book/how-to-dj-right/). Only the publisher description of *How to DJ Right* was checked: it stresses pacing a night and reading a crowd. Its chapter text was not checked.

---


### 3.1 Compatibility checklist (beyond BPM and key)
1. **Groove / rhythmic feel.** Swing versus straight, broken beat versus four-to-the-floor, hi-hat density, percussion pattern. Vande Veire's system chooses, among in-key candidates, the one whose onset pattern over the overlap best matches the current track (DTW on onset detection functions).
2. **Timbre / sound palette.** Analog and warm versus bright and digital, sparse versus dense, dark versus euphoric. Keep consecutive tracks in a style neighborhood (§2.3).
3. **Era and production style.** A 1993 vinyl-mastered house track next to a 2024 hyper-compressed track jumps in loudness and brightness even when BPM and key match. Use gain normalization (ReplayGain or LUFS, as Vande Veire did) and prefer gradual era moves. *Practitioner convention.*
4. **Vocal density.** Avoid stacking vocal-heavy tracks back to back where their vocals would overlap. Alternating vocal and instrumental tracks makes transitions easier and keeps interest (Digital DJ Tips).
5. **Mood / valence.** Dark into happy, or melancholic into euphoric, needs a bridge track or a reset, not a blend.
6. **Energy level** (§2.2).
7. **Familiarity.** Alternate known and unknown tracks. Too many hits in a row feels like a playlist, and too few loses a general crowd.
8. **Function in the set.** Tag tracks by role: opener, builder, bridge, weapon/peak, breather, reset, closer (The Ghost Production). Choose the role first, then the track.
9. **Structural fit for the planned transition.** Does the outgoing track have a usable outro (drums-only, or a quiet bassline)? Does the incoming track have a DJ-friendly intro? If not, plan a short transition type (§7).


### 4.1 Why phrasing matters most
Dance and pop music change in blocks. Something new (an instrument, a fill, a crash, a vocal) arrives about every 16 or 32 beats (DJ TechTools, phrasing 101). Zehren et al., working from interviews with professional DJs, write that EDM is almost always in 4/4 and built from repeated phrases. Sections are made of 2 (or a multiple of 2) phrases, and phrases of 2 (or a multiple of 2) bars, so **every 4-bar boundary is a potential section start**.

**Measured evidence that real DJs phrase-align:**
- Transition lengths in 20,765 real transitions show **peaks at every 32 beats (8 bars)** (Kim et al. 2020) **[measured]**.
- Real DJs agree on cue points to a striking degree. Comparing the cue points different DJs chose in the same track: 23.6% of pairs are identical, 40.4% within 1 bar, 73.6% within 8 bars, and 86.2% within 16 bars (Kim et al. 2020) **[measured]**. Cue choice is not random. It follows shared structural rules.
- In the Raveform dataset of DJ-mix EDM annotations, the most common segment length is about 30 s, which is 16 bars at 128 BPM (Kim et al., TISMIR). This is from the abstract and search summary. The full text was not read.
- Spotify's auto-transition system only allows transition points on downbeats and weights them heavily toward section boundaries. The strongest points are drops, then section boundaries, then plain downbeats (Bittner et al. 2017).


### 4.2 Switch-point rules (from interviews with professional DJs)
From Zehren, Alunno & Bientinesi:
1. **Novelty:** a switch point sits where something changes: rhythmic density, loudness, timbre or harmony. The kick entering as four-to-the-floor is an especially important cue.
2. **Grid:** a switch point is always on a downbeat that begins a 4-bar period. Their annotators placed switch points on 4-bar boundaries, and nearly all misses came from mis-estimated periods or tracks that break the 4-bar grid.
3. **Salience:** the section after the switch must be able to stand on its own: a new melody, bassline or drum pattern that holds attention.
4. DJs may switch 4 or 8 bars *before* the next novelty to build anticipation.

Their rule-based detector found about 9 viable switch-in candidates per track. About 96% were judged usable by experts.


### 4.3 The three cue points of a transition
Zehren and Kim both use this vocabulary:
- **Fade-in start / cue-out of A:** B becomes audible while A still dominates.
- **Switch point:** B becomes the dominant track. This is usually where the bass swap happens.
- **Fade-out end / cue-in complete:** A is gone.

Listeners hear the **switch** (B fully taking over) as "the track change". Human annotators put track boundaries closest to the point where the next track fully appears in 52% of cases, versus 30% at the start of the fade and 18% at the midpoint (Kim et al. 2020) **[measured]**.


### 4.4 Overlay rules
- Phrases of A and B must be **locked**: start B on beat 1 of a phrase in A, at a phrase start in B, so both tracks' phrase boundaries coincide from then on (DJ TechTools, "Phrase mixing"; DJKit "Rule of 32").
- Good structural pairings (EDM Ghost Production; Digital DJ Tips):
  - outro over intro (the classic)
  - breakdown over intro or build
  - end of chorus into verse or intro
  - drums-only over drums-only (safest)
  - only one track carrying melody, bass or vocals at the overlap
- Avoid both tracks having melody **and** bass **and** vocals during the overlap. That gets messy fast.
- **Finish the switch on a phrase boundary.** Home DJ Studio warns against dropping a bassline in the middle of a phrase.


### 4.5 Where to cue in and out, by genre

**House / tech house / techno (120-135 BPM)**
- Structure: intros and outros of 16-32 bars, usually drums-led and DJ-friendly. Elements change every 8 or 16 bars. Techno often runs intro 16-32, build 32-64 (layers added every 8-16), peak 32-64 bars (EDM Ghost Production; DJ.Studio).
- Cue out: start B when A reaches its outro, or 16-32 bars before A's outro (Native Instruments suggests 16 or 32 bars before the outro).
- Cue in: B from its first downbeat, or from the first phrase where the kick is established.
- Blend length: house 16-64 bars. Deep and progressive house sit at the long end (32-64+). Techno uses long hypnotic layering, sometimes 3 or more decks or loops (EDM Ghost Production; DJ.Studio on Jeff Mills).
- Switch (bass swap) where B's bassline arrives, on a phrase boundary.
- Digital DJ Tips puts it practically: on a five-minute outgoing track, start the incoming track with roughly 60-90 seconds of A left.

**EDM / big room / festival (126-132 BPM)**
- Structure: intro → build → drop → breakdown → build → drop → outro. Drops are announced by builds that are easy to see.
- Common moves:
  - mix B in during A's breakdown and land B's drop where A's drop would have been (drop swap)
  - cut from A's breakdown straight into B's build (a classic main-stage move)
  - "power block": jump straight to the most recognisable sections
- Shorter transitions (8-16 bars). Keys matter a little less because melodies are often minimal (beatif.studio; We Are Crossfader; Mixed In Key).

**Drum & bass (170-176 BPM)**
- Structure: intro, build, drop into the main section, breakdown, second build and drop, outro. Phrases are multiples of 8 bars, and segments are whole numbers of phrases (Vande Veire & De Bie, citing *How to DJ Right*). Producer Danny Byrd says his main drop is usually about 48 bars (three 16-bar blocks), with the last block stripped back on purpose so DJs can bring the next track in.
- Measured-from-practice templates (Vande Veire & De Bie):
  - **Double drop:** cue both tracks 16 bars before a drop. Fade-in 16 bars, fade-out 32 bars. Both drops land on the same downbeat.
  - **Rolling:** cue A 32 bars before its next high→low boundary (end of drop). Cue B on the downbeat 16 bars before its drop. Fade-in and fade-out 16 bars each. B's drop continues A's energy.
  - **Relaxed:** cue A 16 bars before its next high→low boundary. B starts from its beginning. Fade-in and fade-out 16 bars each. This gives the floor a rest.
- Double drop by hand: set cues the same number of bars (8, 16 or 32) before each drop, so starting B at A's cue lands both drops together (DJ Gear 2K; Home Music Maker).

**Hip-hop / R&B / open format (70-105 BPM; often 85-100)**
- Structure: 16-bar verses and 8-bar hooks are typical (practitioner convention). Short intros, sometimes vocal from bar 1.
- Transitions are short: cut on the one, echo out, quick 4-8 bar blends from hook to hook (Native Instruments; DJ Record Pool; CMUSE). Big BPM changes are handled with cuts and echoes, not stretching.
- Cue out: at the end of a hook or verse, **never mid-sentence** (DJ Record Pool). Cue in: B's first downbeat, or straight into B's hook if B is recognisable.

**Pop / radio / wedding / Top 40**
- Structure: verse, pre-chorus, chorus, often in 4- and 8-bar blocks. Many radio edits end cleanly or abruptly.
- Moves: end-to-end on the downbeat, a fade from the second chorus, a cut at the end of a chorus, or a short single-phrase beatmix over drum-dominated sections (Digital DJ Tips, "Five Basic DJ Transitions").
- Fade guidance: drop the volume sharply at first so the change is obvious, then fade more slowly over about 10-15 seconds, finishing near the end of the current 8-bar phrase. Start the new track on the downbeat of a new phrase.

**Bollywood / Punjabi / desi (limited source material)**
- Few rigorous sources exist. Available guides say desi DJs lean on **edits**: re-drums and club edits for stronger percussion, intro/outro edits to make vocal-led songs blendable, and "transition edits" that move between tempo ranges inside one track. Libraries are organised by event moment, energy, language and function, not just artist (Lunarkal, Bollywood DJ edits). Wedding sets are planned around ceremony moments (baraat is high energy with live dhol; cocktail hour is soft, acoustic, lounge) (DJ Raj; SoDJLA).
- **Practitioner conventions, not verified by a cited source:**
  - Many Bollywood songs open with free-tempo alaap, shayari or orchestral intros that have no stable beat grid. Cue past them, or cut or echo into the first stable downbeat.
  - Songs are vocal-dense with short instrumental gaps, so prefer cuts, echo outs and hook-to-hook switches over long blends.
  - Bhangra and dhol-driven tracks pair well with 4-beat dhol fills used as transition punctuation.
  - Tempos across Bollywood catalogues vary widely, so use cuts or edits between tempo groups rather than stretching beyond ±6%.


### 4.6 Aligning drops
- Drop-to-drop alignment requires both tracks to be cued the **same number of bars** before their drops (8, 16 or 32).
- Two full drops with full bass at once sounds muddy even in compatible keys. Keep the bass of one track cut (B comes in with low EQ at 0), then hand the bass over after 8, 16 or 32 bars. Some DJs alternate the bass between tracks every couple of beats as a deliberate effect (DJ Gear 2K summary).
- We Are Crossfader warns that if drops land on top of each other unintentionally, or if a track comes in too early or late, the impact is lost. Alignment must be exact to the downbeat.

Sources: DJ TechTools, "How to DJ 101: Why You Must Understand Phrasing" (https://djtechtools.com/2014/11/16/how-to-dj-101-why-you-must-understand-phrasing/) and "Phrase Mixing" (https://djtechtools.com/2015/10/22/phrase-mixing-throwback-thursday-dj-technique/); Zehren, Alunno & Bientinesi, "Automatic detection of cue points for DJ mixing" (https://arxiv.org/abs/2007.08411; Computer Music Journal 46(3), https://doi.org/10.1162/comj_a_00652); Kim et al. ISMIR 2020 (above); Raveform, TISMIR (https://transactions.ismir.net/articles/10.5334/tismir.288); Bittner et al. 2017 (above); Vande Veire & De Bie 2018 (above); Digital DJ Tips, "Five Basic DJ Transitions" (https://www.digitaldjtips.com/rock-the-dancefloor/five-basic-dj-transitions/); Native Instruments, "5 basic DJ transitions" (https://blog.native-instruments.com/dj-transitions/); EDM Ghost Production, "DJ Phrasing" (https://edm-ghost-production.com/dj-knowledge-base/dj-phrasing-when-to-mix) and "Mixing by Genre" (https://edm-ghost-production.com/dj-knowledge-base/mixing-by-genre); DJ.Studio techno guide (https://dj.studio/blog/dj-techno-music); DJKit "Rule of 32" (https://www.djkit.com/blogs/news/djing-rule-of-32); Home DJ Studio, "The Complete Guide To DJ EQing" (https://homedjstudio.com/dj-eqing/); beatif.studio big room guide (https://beatif.studio/mag/blog/what-is-big-room/); We Are Crossfader, "How to mix EDM" (https://wearecrossfader.co.uk/blog/how-to-mix-edm/); DJ Gear 2K, double drop (https://djgear2k.com/double-drop-mixing-guide/); Home Music Maker, double drop (https://www.homemusicmaker.com/what-is-a-double-drop); Benztown / Danny Byrd production diary (https://benztown.com/do-one-of-the-hardest-dj-techniques-in-a-few-minutes-or-do-a-double-drop-in-pro-tools-andres-production-diary-part-30/); DJ Record Pool, transition techniques (https://djrecordpool.com/dj-transition-techniques/); CMUSE transition bar calculator (https://www.cmuse.org/dj-transition-bar-calculator); Lunarkal, Bollywood DJ edits (https://lunarkal.com/bollywood-dj-edits-desi-weddings/); rekordbox Phrase Edit guide (https://cdn.rekordbox.com/files/20200312172204/rekordbox5.1.0_Phrase_Edit_operation_guide_EN.pdf).

**Mapping to rekordbox-style labels.** Pioneer's phrase analysis labels sections Intro / Up (build) / Down (breakdown) / Chorus (the "uplifting" section, i.e. the drop in EDM) / Bridge / Verse / Outro. It also detects "Fill-in" in the last ≤4 beats before a phrase change. A track-level mood (High / Mid / Low) decides whether EDM-style or pop-style labels apply. If the analyzer produces the same labels, treat "Chorus" in High-mood tracks as the drop, and treat a fill-in as a strong signal that a phrase boundary follows.

---


### 5.1 How much tempo change is acceptable
- **[measured] What real DJs do (1,557 mixes):** 86.1% of tracks are played within ±5% of their original tempo, 94.5% within ±10%, and 98.6% within ±20%. The distribution is sharply peaked at zero (Kim et al. 2020).
- **[measured] Listener discomfort (96 subjects):**
  - Gradually stretching a pop song, the average point where listeners noticed discomfort was a speed-up of ×1.227 or a slow-down of ×0.852.
  - Discomfort reports peaked at ×1.10 and ×0.90. Inside the ±10% band, only about 11-15% of subjects felt discomfort.
  - **Listeners are more sensitive to slowing down than speeding up.**
  - A better time-stretch algorithm mattered near the original tempo (inside ±10%) (Ishizaki et al., ISMIR 2009).
- **Key lock / master tempo artifacts (practitioner reports):**
  - Up to about ±3% is clean either way.
  - Around 5-6%, artifacts start to show on some material, especially transients and reverb tails.
  - Beyond about 8% the stretch is clearly audible.
  - Without key lock, pitch moves about 1 semitone per 6% of tempo change, and ±2% or less is hard to notice (OpenKeyScan; Mixgraph; Pioneer and VirtualDJ forum users).
- **[measured] Key transposition is rare:** only 2.5% of tracks in real mixes were transposed at all. Of those, 94.3% moved by just 1 semitone (Kim et al. 2020). DJs leave master tempo on and play the original key.

**Planner policy:**
- **Preferred** stretch ≤ ±3%.
- **Normal ceiling** ±6%.
- **Hard ceiling** ±8%, and only while the stretched track is mostly hidden (under the other track, in a breakdown, or behind an FX wash).
- Slow-downs get a stricter ceiling than speed-ups (e.g. −5% / +6%).
- **Split the stretch across both tracks.** Ishizaki's "optimal tempo adjustment" speeds A up and slows B down (e.g. A +5% and B −5% instead of B −10%), which lowers measured discomfort.
- **Change the master tempo gradually.** Spotify's renderer ramps tempo smoothly from A's tempo to B's across the transition beats. Ishizaki also inserted ramp periods between the original and adjusted tempo. A sudden tempo jump in the middle of a groove is a tell.
- Bittner et al. only tested auto-transitions on pairs within 5 BPM, which is about 4% at 125 BPM.
- Mixxx's AutoDJ only uses pitch sync when BPMs are within 6% of each other.
- Beyond about an 8% gap, use a technique that doesn't depend on tempo: echo out, cut on the one, spinback, or a half/double-time bridge (VibesDJ transitions guide).


### 5.2 Half-time and double-time
- Exactly 2:1 tempo ratios share a beat grid: 70↔140, 87↔174, 100↔200. One bar of the slow track spans two bars of the fast one, so they can be mixed without moving the pitch fader (Digital DJ Pool; Mixgraph; DJ.Studio).
- Pairings that work: hip-hop 87 into DnB 174; trap 70 into dubstep 140 (both already think in half-time).
- No direct relation, e.g. house 124 → DnB 174: echo out of house into something around 87 (a hip-hop or half-time break), then blend that up to 174.
- **Analyzer warning:** software often labels DnB at 85 or dubstep at 70. Normalise tempo octaves before comparing BPMs, or a planner will "stretch" a track by 100%. Ishizaki et al. point out that double/half tempo errors from beat trackers would otherwise double the requested adjustment.


### 6.2 Moves, from safest to boldest

| Move | Example from 8A | Camelot op | Musical meaning | Use |
|---|---|---|---|---|
| Same key ("power block") | 8A → 8A | 0 | identical | Safest; holds the mood |
| ±1 same letter | 8A → 7A / 9A | ±1 | Fifth down/up (subdominant/dominant) | Safe, smooth |
| Relative major/minor | 8A → 8B | A↔B | Same notes, mood flip | Safe; changes colour (minor→major lifts, major→minor darkens) |
| Diagonal | 8A → 9B, 8B → 7A | ±1 and letter swap | Close but less safe | Use with care |
| **Energy boost +2** | 8A → 10A | +2 | Whole tone up | Noticeable lift. MIK: every 20-30 min, not all the time |
| **Semitone up +7** | 8A → 3A | +7 | One semitone up | Strong lift. Use sparingly, ideally over percussion-only overlap |
| Going −2 | 8A → 6A | −2 | Whole tone down | Signals winding down (MIK book) |
| "Jaws" −5, "Pay attention" −3 | 8A → 3A / 5A | −5 / −3 | Advanced moves listed by MIK | Rare, deliberate |

Notes:
- Mixed In Key's older book describes the energy boost as going up 1 or 2 semitones: +7 on the wheel for one semitone, +2 for two. It says two semitones tends to be the safer of the two.
- Vande Veire's auto-DJ allows same key, fifth up or down (±1), and relative key. It widens the pool by pitch-shifting tracks that are 1 semitone away from a compatible key.
- Third-party guides warn that jumps beyond +2 increase clash risk. Some (TrackScore) label +7 itself as "the energy boost". Both conventions exist.


### 7.12 Choosing a transition (decision guide)

| Situation | First choice | Second choice |
|---|---|---|
| Both tracks have drum-led outros/intros, same genre, ≤3% stretch | Long blend + bass swap (7.1/7.2) | 3-band EQ swap |
| Busy tracks, no clean intro/outro, same tempo | Single-phrase beatmix or filter fade | Echo out + cut |
| Tempo gap >6-8% with no 2:1 relation | Echo out or cut on the one | Brake/spinback (rare) or bridge track |
| 2:1 tempo relation | Half/double-time blend over drums | Cut on the one |
| Vocal on both sides at the overlap | Echo out on the last word → B on the downbeat | Move cue points so vocals don't overlap |
| Peak moment, DnB/bass music, compatible keys | Double drop or drop swap | Loop roll into B's drop |
| Need to calm the floor | Relaxed transition into B's intro | Fade or end-to-end into a breather |
| Hip-hop / open format | Cut on the one, quick 4-8 bar blend hook to hook | Echo out |
| Track A is clearly not working | Fade or quick cut to a safe floorfiller | |

Sources: Digital DJ Tips, "Five Basic DJ Transitions" and house guide (above); Native Instruments, "5 basic DJ transitions" (above); Vande Veire & De Bie 2018 (above); Kim, Yang & Nam, NIME 2021 (https://nime.pubpub.org/pub/g7avj1a7) and DAFx 2022 (above); Home DJ Studio EQ guide (above); Digital DJ Pool, "DJ EQ Mixing for Beginners" (https://digitaldjpool.com/blog/dj-eq-mixing-for-beginners/) and "7 DJ Transitions" (https://digitaldjpool.com/blog/dj-transitions-for-beginners/); VibesDJ transitions (above); DJ Record Pool (above); We Are Crossfader (above); DJing Tips, "Backspins, Stops and Power-Offs" (https://www.djingtips.com/how-to-dj/backspins-stops-and-power-offs/); ZipDJ, DJ acapellas (https://www.zipdj.com/blog/dj-acapellas); Digital DJ Tips, "How To DJ With Acapellas" (https://www.digitaldjtips.com/how-to-dj-with-acapellas/); DJ.Studio, acapellas (https://dj.studio/blog/acapellas-for-djs); Chen et al., "Automatic DJ Transitions with Differentiable Audio Effects and GANs", ICASSP 2022 (https://arxiv.org/abs/2110.06525). Chen et al. model a DJ transition as exactly a fader plus 3-band EQ per track, learned from real mixes, which supports the EQ/fader parameterisation used here.

---


## 8. Amateur tells: slop detectors

Each tell below says what it sounds like, why it happens in an automated plan, and how to detect it from data.

1. **Clashing basslines.** Both lows open at once, giving mud and phase-cancelled kicks. *Detect:* the sum of low-band gains > 1.0 for more than 1 beat, outside a deliberate bass-alternation effect. Guides call bass clashes especially obvious on club systems and an instant sign of inexperience.
2. **Two vocals at once.** Digital DJ Tips calls this a "complete no-no". *Detect:* both tracks' vocal-presence flags are true and both are audible (fader × mid gain > 0.3) for ≥2 bars (Vande Veire tolerates 1).
3. **Mixing mid-phrase.** B enters, the switch happens, or A exits at a bar that isn't a phrase boundary. The music lurches. *Detect:* event bar index mod 8 ≠ 0 relative to that track's phrase grid (allow mod 4 for 4-bar-period material).
4. **Flamming / galloping kicks.** A bad beat grid or downbeat offset (beat 1 on beat 3). The #1 curator complaint about auto-transitions. *Detect:* low grid confidence or inter-onset drift >10 ms during overlap; downbeat mismatch.
5. **Same transition every time.** Identical length, identical EQ curve, identical filter or echo. Instantly reads as a machine. *Detect:* a type repeated 3 times in a row, or one type >50% of the set; transition lengths all equal.
6. **Equal-length, symmetric, linear crossfades everywhere.** Real DJs move one control at a time, in steps tied to the music, with a switch moment. *Detect:* every transition is a linear constant-power crossfade with no EQ; per-band curves identical.
7. **Volume hole or bump in the middle of the transition.** Both tracks at half, or both at full. Real mixes keep roughly constant energy across transitions. *Detect:* short-term loudness during the transition dips >3 dB or rises >2 dB versus the surrounding solo sections.
8. **Overused FX.** Filter sweeps every 8 bars, reverb on everything, echo on every exit, rolls in every transition, air horns. *Detect:* FX active in >40% of transitions or >15% of total time; any single FX in >3 consecutive transitions.
9. **EQ boosted above unity.** Boosting the low end of mastered tracks causes problems (DJ TechTools). *Detect:* any gain > 1.0.
10. **Abrupt volume dips or fader jumps without musical reason.** *Detect:* gain discontinuities > 0.3 not on a downbeat and not part of a cut recipe.
11. **Cutting tracks off too early.** Exiting before the track has made its point or finished its section. *Detect:* play time below the genre minimum; exit not at a section end.
12. **Playing too many hits back to back** / all the bangers first. No contrast and nowhere left to go. *Detect:* more than 3-4 consecutive tracks at energy ≥8; the energy maximum inside the first 30% of a non-peak-slot set.
13. **No dynamics.** Flat energy for an hour, or a straight ramp up. *Detect:* standard deviation of per-track energy too low, or the energy curve monotonic with no dips.
14. **Big energy or genre jumps with a smooth blend.** A long blend between incompatible grooves or moods (e.g. dark techno into tropical house). *Detect:* style-embedding distance above threshold combined with overlap >8 bars.
15. **Tempo yo-yo.** Master BPM jumping up and down between tracks, or large sudden tempo changes. *Detect:* |ΔBPM| > 3% inside a groove without a ramp; direction reversals across consecutive transitions with no musical reason.
16. **Chipmunk / sludge.** Stretching beyond about 8%, or slowing a vocal track heavily. *Detect:* stretch beyond the limits in §5.
17. **Key clash over sustained melody or vocal.** *Detect:* Camelot distance ≥2 (not a deliberate +2 or +7 boost) with melodic overlap ≥4 bars.
18. **Doubled hi-hats / harsh top end.** Both highs at full during a long overlap. *Detect:* the sum of high-band gains > 1.3 for more than 8 bars.
19. **Entering on a weak section.** Switching into a quiet, non-salient part of B, so the mix sags at the moment B should take over. *Detect:* the energy of B's section after the switch < 0.4 × B's max (Zehren's salience threshold used 0.4 × max harmonic energy).
20. **Over-tidy "perfect" planning.** Every transition exactly 16 bars, every key ±1, every energy +1. Real sets have deliberate exceptions: resets, boosts, cuts. *Detect:* zero variance on any of those dimensions over an hour.
21. **Drop collision by accident.** Two drops layered unintentionally, or B's drop landing a beat or bar off. *Detect:* overlapping high-energy sections without an explicit double-drop type, or drop offset ≠ 0 beats.
22. **Ending into silence or a hard stop at the end of the set.** *Detect:* the final track cut mid-section.

Sources: Digital DJ Pool, "11 Beginner DJ Mistakes" (https://digitaldjpool.com/blog/dj-mistakes-beginners-make/); DJs On Demand, common mistakes (https://www.djsondemand.co.uk/the-most-common-dj-mistakes-beginners-make/); The DJ Revolution, "20 DJ mistakes" (https://www.thedjrevolution.com/dj-mistakes/); ZipDJ, DJ mistakes (https://www.zipdj.com/dj-mistakes/); DJ TechTools bad habits (above); Digital DJ Tips house guide (above); Bittner et al. 2017 (above); Kim, Yang & Nam DAFx 2022 (above); Vande Veire & De Bie 2018 (above); Zehren et al. (above).

---
