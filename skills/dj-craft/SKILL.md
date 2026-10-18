---
name: dj-craft
description: Reference for planning DJ mixes that sound like a tasteful, experienced human DJ rather than an algorithm. Covers DJ mindset, set programming and energy arcs, track selection, phrasing and cue placement by genre, beatmatching and tempo limits, harmonic (Camelot) mixing, exact transition recipes with bar-by-bar EQ/fader/FX automation, amateur "slop" tells, machine-checkable scoring rules with thresholds, and a 1-10 listening rubric for judging rendered transitions. Use whenever planning, scoring, critiquing, or rendering a mix from analyzed track data (BPM, beat/downbeat grid, Camelot key, energy curve, sections, vocal presence).
---

# DJ Craft: planning mixes that sound human

This file is the knowledge base for an AI DJ that plans mixes from analyzed track data: BPM, beat and downbeat grid, Camelot key, energy curve, section labels (intro / verse / chorus / build / drop / breakdown / outro), and vocal presence. **The top goal is that mixes never sound like AI slop.** They should sound like a DJ with taste who has played a thousand nights.

Everything here is paraphrased from the sources cited at the end of each section. Where a claim is practitioner convention that no single source pins down, it says so. Numbers from academic studies of real DJ mixes are marked **[measured]**.

**Conventions used below**
- 1 bar = 4 beats (all genres covered here are 4/4). "Phrase" means an 8-bar block (32 beats) unless stated otherwise. In dance music, sections are usually 8, 16 or 32 bars.
- "Outgoing" = track A (currently playing). "Incoming" = track B.
- EQ gains are linear, 0.0 = killed and 1.0 = unity (12 o'clock). **Nothing goes above unity.**
- "Low / mid / high" follow a typical 3-band DJ mixer: low shelf around 180 Hz, mid peak around 1 kHz, high shelf around 3 kHz. These are the Allen & Heath Xone:96 settings used by Kim, Yang & Nam (DAFx 2022).

---

## 1. The DJ's mindset and taste

### 1.1 What a DJ actually does
A DJ builds an experience that unfolds over time, for a particular room and moment, out of other people's records. Real DJs work in three steps: matching beats and tempo, choosing cue points, and shaping the handover with faders, EQ and effects (Kim, Yang & Nam 2022). The technical part is the easy part. What separates great DJs from mediocre ones is **judgment**: what to play, when, for how long, and when to do nothing at all.

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

## 2. Set programming

### 2.1 The arc of a night
A professional mix usually moves in stages. It starts relaxed, builds energy with increasingly intense tracks, reaches a climax, eases off to let people rest, and may build again to a second peak. Vande Veire & De Bie describe this pattern, citing *How to DJ Right*.

| Phase | Typical share of set | Energy (MIK 1-10) | Tempo | What it's for |
|---|---|---|---|---|
| Warm-up / opening | first 20-30% | 3-5 | Low end of genre range. RA cites staying under ~124 BPM for house openers | Pull early dancers off the bar. Deep, groovy, few anthems |
| Build | 25-35% | 5-7 | Climbing gently | Add floorfillers. Energy rises one step at a time |
| Peak | 20-30% (usually the last third, not the end) | 7-9 (MIK suggests 9 as a climax, "if you even want to go that high") | Top of range | Biggest tracks, tighter mixing, less breathing time between tracks |
| Cool-down / close | last 10-15% (if closing the night) | Falling to 4-6 | Easing down | Lower tempo and intensity so people leave happy (DJ TechTools) |

Context changes this. A warm-up set should never peak: it should hand over at an energy the headliner can build on. A peak-time guest set starts at 6 to 7. A wedding uses peaks and valleys around the event's moments (DJ Lou Paris; Indian wedding sources describe distinct energy for baraat, cocktail hour, and dance floor).

### 2.2 Energy steps
- **Default move: same energy or ±1 level** between consecutive tracks. "5 → 5" holds the mood and "5 → 6" gives a smooth lift (Mixed In Key, "Use energy level detection").
- Mixed In Key notes that a key match does **not** make an energy jump feel right. A low-energy track and a high-energy track can be harmonically compatible and still feel too sudden.
- One third-party guide (VibesDJ) suggests giving each new level 3 to 4 tracks before climbing again. Treat this as a heuristic.
- **Reset:** sometimes a deliberate drop in energy, or even a "hard reset", is the right move for a bored crowd (Digital DJ Tips, "How DJs always know what song to play next"). Make resets rare and deliberate, then build again from a compatible key.
- After several big tracks in a row, insert a short low-energy moment before the next anthem (Mixed In Key, "power block" tip).

### 2.3 Contrast versus continuity
- Real DJ mixes stay inside a fairly small "style neighborhood" (a blend of timbre, mood and energy) compared with the whole library. Vande Veire & De Bie measured this by plotting a spectral-contrast style descriptor over the course of professional DnB mixes **[measured, qualitative]**. Their auto-DJ copies it by pulling each next track toward a set-wide style centroid (weight 0.4). It also pushes slightly *away* from the previous track (weight −0.1), so the style keeps flowing instead of standing still.
- Continuity comes from groove, tempo, timbre and genre. Contrast comes from vocal versus instrumental, familiar versus unknown, tension versus release, and energy steps. Digital DJ Tips suggests alternating vocal and instrumental tracks, and alternating well-known and lesser-known tracks.
- In Spotify's study, professional curators preferred playlists sequenced for key, tempo and timbre consistency. Random orders produced more pairs that curators marked "abrupt" (Bittner et al., ISMIR 2017) **[measured]**.

### 2.4 Tracks per hour (by genre)

| Style | Play time per track | Tracks / hour | Notes |
|---|---|---|---|
| Deep / progressive house, melodic techno | 4-6 min | 10-15 | 32-64+ bar blends |
| House / tech house | 3.5-5 min | 12-20 | Mixgraph's tech house example: ~22/hour with ~45 s overlaps |
| Techno | 3-5 min | 12-18 | Often layered or looped |
| Drum & bass | 2-3 min | 20-30 | Mixgraph: 25+ |
| Big room / festival EDM | 2-3 min | 20-30 | "Power block": jump to the best parts |
| Hip-hop / open format (quick mixing) | 1-2 min | 25-50 | Tracks cut early, hook to hook |
| Hip-hop played near full length / radio-style pop | 3-4 min | 12-18 | |
| **Measured average (1,557 real mixes on 1001Tracklists, mostly EDM)** | ~4 min | **~15.5 tracks per 60.5-min mix** | Kim et al., ISMIR 2020 **[measured]** |

Formula: tracks per hour ≈ 60 / average play time in minutes.

### 2.5 Avoiding monotony
- Vary transition type and length. Vande Veire's auto-DJ uses a state machine for this. After a "relaxed" transition, the next is rolling with probability 0.7 or double drop with 0.3. After a rolling transition, the next is relaxed 0.2 or rolling 0.8. After a double drop, the same 0.2 / 0.8 split applies, and double drops are never allowed directly after a rolling transition or another double drop, to avoid stacking too many tracks.
- Don't fire every big track in the first minutes. Save some of the best for the final 20 minutes (DJ TechTools).
- Regulars notice repetition, so rotate pre-planned groups of three (DJ TechTools, "triads").

Sources: Vande Veire & De Bie, "From raw audio to a seamless mix", EURASIP J. Audio Speech Music Proc. 2018:13 (https://asmp-eurasipjournals.springeropen.com/articles/10.1186/s13636-018-0134-8); Kim et al., "A Computational Analysis of Real-World DJ Mixes using Mix-To-Track Subsequence Alignment", ISMIR 2020 (https://arxiv.org/abs/2008.10267); Bittner et al., "Automatic Playlist Sequencing and Transitions", ISMIR 2017 (https://archives.ismir.net/ismir2017/paper/000086.pdf); Mixed In Key, "Use energy level detection" (https://mixedinkey.com/workflows/use-energy-level-detection/), "Sorting playlists by Energy Level" (https://mixedinkey.com/harmonic-mixing-guide/sorting-playlists-by-energy-level/), "5 Mixing Techniques Every DJ Should Know" (https://mixedinkey.com/wiki/5-mixing-techniques-every-dj-should-know/); Mixgraph set length calculator (https://www.mixgraph.io/tools/set-length-calculator); VibesDJ, "How many songs for a DJ set" (https://vibesdj.io/learn/techniques/how-many-songs-for-a-dj-set) and "Build a set by energy" (https://vibesdj.io/learn/techniques/how-to-build-a-set-by-energy); DJ TechTools, reading the floor and bad habits (above); RA opening DJ (above); Digital DJ Tips, "How DJs Always Know What Song To Play Next" (https://www.digitaldjtips.com/how-djs-always-know-what-song-to-play-next-without-ever-panicking/); DJ Lou Paris, "How I Mix At A Wedding" (https://djlouparis.com/for-djs/philosophy/how-i-mix-at-a-wedding/); DJ Raj, Indian wedding music flow (https://djraj.com/how-indian-wedding-djs-create-perfect-music-flow-for-each-ceremony/).

---

## 3. Track selection taste ("selecting > mixing")

A perfect blend of two tracks that don't belong together still sounds wrong. A slightly rough blend of two tracks that belong together sounds fine. In Ishizaki et al.'s listening tests, some song pairs were unacceptable to listeners no matter how well they were tempo-matched. The authors conclude that tempo is only one of many factors **[measured, qualitative]**. In Bittner et al.'s curator test, 4.3% of bad transitions were blamed simply on "contrasting songs".

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

### 3.2 Selection procedure (adapted from Vande Veire & De Bie's pipeline)
1. Filter by tempo compatibility: within ±6% of native tempo, or a half/double-time relation (§5).
2. Filter by harmonic compatibility (§6), **only where melodic content will actually overlap**.
3. Keep the K closest in style to the target style, a mix of set centroid and recent trajectory.
4. Choose cue points for the intended transition type (§4, §7).
5. Reject candidates that cause vocal overlap of 2 or more bars (Vande Veire tolerates exactly 1 bar).
6. Among the rest, prefer the best rhythmic (onset pattern) similarity over the overlap region.
7. Check the energy step and the arc target.

Sources: Ishizaki, Hoashi & Takishima, ISMIR 2009 (https://archives.ismir.net/ismir2009/paper/000043.pdf); Bittner et al. 2017 (above); Vande Veire & De Bie 2018 (above); Digital DJ Tips, "How DJs Always Know What Song To Play Next" (above); The Ghost Production, reading-the-crowd mistakes (https://theghostproduction.com/reading-the-crowd-mistakes-dj-sets/); Mixed In Key energy workflow (above).

---

## 4. Phrasing and structure

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

## 5. Beatmatching and tempo

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

### 5.3 Beat-grid quality is the #1 technical risk
- In Spotify's curator test of auto-transitions, the most common reason for a "Bad" rating was **"beats do not align"** (15.2% of pairs), caused by beat-tracking errors. Bittner et al. conclude that beat and downbeat tracking errors were the main limit on quality **[measured]**.
- Ishizaki et al. found that pairs where one track's strong beats landed on the other's weak beats (a downbeat offset by 2 beats) scored poorly even when tempo was perfect. Downbeat alignment, not just beat alignment, is essential **[measured]**.
- Zehren et al. note that the downbeat is easily confused with beat 3 in EDM.
- **Policy:** only plan long overlaps (more than 1-2 bars of audible kicks together) where both grids are confident and drift stays under ~10 ms across the overlap. Otherwise use a short overlap, cut, or echo out. The 10 ms figure is a heuristic: drift around 20-30 ms between two kicks starts to sound like flamming. *Practitioner convention.*

Sources: Kim et al. 2020 (above); Ishizaki et al. 2009 (above); Bittner et al. 2017 (above); OpenKeyScan, "Key and BPM guide" (https://www.openkeyscan.com/key-and-bpm-guide); Mixgraph pitch/tempo calculator (https://www.mixgraph.io/tools/pitch-tempo); Pioneer DJ forum thread on master tempo artifacts (https://forums.pioneerdj.com/hc/en-us/community/posts/205248123-DJM900NXS2-Pitch-effect-has-noticeable-artifacts); VirtualDJ forum on keylock quality (https://virtualdj.com/forums/198211/VirtualDJ_8_bug-report_Forum/Keylock__pitch_quality.html); Mixxx AutoDJ wiki (https://github.com/mixxxdj/mixxx/wiki/gsoc2012_autodj_features); VibesDJ transitions guide (https://vibesdj.io/dj-tools/dj-transitions); Digital DJ Pool BPM guide (https://digitaldjpool.com/blog/dj-bpm-guide/); Mixgraph double-time glossary (https://www.mixgraph.io/glossary/double-time); DJ.Studio tempo change techniques (https://dj.studio/blog/dj-tempo-change-techniques); Zehren et al. (above).

---

## 6. Harmonic mixing (Camelot)

### 6.1 The wheel
The Camelot wheel numbers 12 positions 1-12, each with A (minor) and B (major). Neighbouring numbers are a perfect fifth apart, and A/B at the same number are relative minor/major.

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

### 6.3 When key matters, and when to break the rules
- **Key only matters where melodic or harmonic content overlaps.** If the transition is finished before B's melody or bass arrives, key is irrelevant. Mixing every transition in key even when nothing overlaps is listed as a mistake (Digital DJ Tips; Digital DJ Pool).
- Overlaps that forgive key clashes:
  - percussion-only handoffs
  - quick cuts (open-format DJs break the wheel "all night" this way)
  - sparse breakdown-to-intro blends
  - genre changes, where the contrast masks the clash
  - deliberate tension (Digital DJ Pool; Setflow; Djoid)
- Overlaps that punish key clashes: **vocal over melody**, sustained pads, melodic progressive or trance leads, long breakdowns with chords.
- **[measured]** In Spotify's curator evaluation (pairs within 5 BPM, transitions on downbeats), "key clash" was flagged for **0%** of transitions, while beat misalignment was 15%. Within a reasonable selection, rhythm and structure errors are far more audible than key errors.
- Key detection is imperfect. Digital DJ Pool cites published accuracy of 41-86% across tools. Two tracks in the "same key" can still clash. Treat the wheel as probabilities, not guarantees, and avoid long melodic overlaps when key confidence is low.
- Setflow: a perfectly harmonic transition with a 20 BPM jump sounds worse than a small key clash at the same tempo. **Rhythm beats harmony.**
- Keymixing is "a tool, not a rule" (Digital DJ Tips). A noticeable key change inside a well-executed mix is usually accepted.

Sources: Mixed In Key, "Energy Boost mixing tutorial" (https://mixedinkey.com/harmonic-mixing-guide/energy-boost-dj-mixing-tutorial/), "Interactive Camelot Wheel" (https://mixedinkey.com/camelot-wheel/), "Change DJ Set Energy With the Camelot Wheel" (https://mixedinkey.com/workflows/change-energy-with-camelot-wheel/), "Use Advanced Harmonic Mixing Techniques" (https://mixedinkey.com/book/use-advanced-harmonic-mixing-techniques/); Vande Veire & De Bie 2018 (above); Bittner et al. 2017 (above); Digital DJ Pool, "Harmonic Mixing Explained" (https://digitaldjpool.com/blog/harmonic-mixing-camelot-wheel/); Setflow, harmonic mixing (https://www.setflow.app/blog/harmonic-mixing-camelot-wheel); Djoid, "Harmonic Mixing Is Not Enough" (https://www.djoid.io/articles/harmonic-mixing-is-not-enough-why-energy-matters-more-than-key); TrackScore, Camelot guide (https://trackscore.ai/blog/camelot-wheel-harmonic-mixing); Digital DJ Tips house guide (above); DJ TechTools forum threads on harmonic mixing (https://forum.djtechtools.com/t/harmonic-mixing/38388).

---

## 7. Transition recipes

**How to read the recipes:**
- Bars are counted relative to the transition start T (bar 0 = the downbeat where B first becomes audible), unless stated otherwise.
- "A.low = 1→0 over bars 8-9" means a linear or eased ramp between those bar lines.
- All starts and ends fall on downbeats. Every bar count is a multiple of 4, normally 8 or 16.

**How real DJs actually shape transitions [measured]:**
- Estimates from real mixes suggest **about 72% of transitions use EQ together with faders, and about 28% use faders/crossfader only** (Kim, Yang & Nam, NIME 2021; a model-fit estimate, not ground truth).
- **Real DJ mixes keep relatively constant energy through the transition.** Synthetic transitions that dip in the middle reconstruct real mixes poorly (Kim, Yang & Nam, DAFx 2022). **No loudness hole in the middle.**
- A realistic model of hand movement: at most about one gain control changes per hand in any ~4-second window, with gains monotonic (A only goes down, B only goes up). Kim et al. built their synthetic DJ data this way.
- Vande Veire's hand-designed crossfade, which DnB fans rated well:
  1. During the fade-in, B's volume rises gradually while **its bass and treble stay almost entirely cut**.
  2. At the end of the fade-in, a **switch**: B's bass and treble come up quickly to full while A's bass and treble are cut at the same moment.
  3. A's volume then fades over the remaining bars.
  The result: only one track's bass and treble are heard at any moment.

### 7.1 Long blend (intro/outro layering)
- **When:** house, deep and progressive house, techno, melodic techno, trance. Both tracks have drum-led outros and intros. Similar groove and compatible key if melodies overlap.
- **Length:** 32-64 bars (house 16-64; deep/progressive 32-64+).
- **Automation, 32-bar version** (A in its outro, B from its intro):
  - Bar 0: B starts at phrase start. B.fader 0.6, B.low 0, B.mid 0.6, B.high 0.5. B's hats and percussion peek in.
  - Bars 0-8: B.fader 0.6→1.0. B.high 0.5→1.0 by bar 8.
  - Bars 8-16: B.mid 0.6→1.0. A.high 1.0→0.6 (A's hats step back so the hats don't double).
  - **Bar 16 (phrase boundary): bass swap.** A.low 1→0 and B.low 0→1 within 1 beat, or a fast 1-2 bar crossover.
  - Bars 16-24: A.mid 1.0→0.5. A.fader 1.0→0.7.
  - Bars 24-32: A.fader 0.7→0. Fully out at bar 32 (phrase boundary). Then reset A's EQ to neutral.
- **Pitfalls:** double hi-hats (cut one track's highs), two melodies fighting, kicks flamming from a bad grid, an overlap long enough to get muddy, a loudness bump at the overlap.

### 7.2 Bass swap ("bassline swap beatmix")
- **When:** house, techno, trance, disco, DnB. The core of most EDM blends. Lets you overlap longer without bass clash.
- **Length:** 16-32 bars of overlap, with the swap itself at one phrase boundary.
- **Automation (16 bars):**
  - Bar 0: B in with B.low = 0, fader rising to 1.0 over 4-8 bars.
  - Bar 8 or 16: on the downbeat where B's bassline arrives, or the phrase start just before it, **simultaneously** A.low 1→0 and B.low 0→1. Swap in ≤1 beat for punchy material. Over 1-2 bars if B's bass is weak, so A's bass fades progressively while B's rises (Home DJ Studio).
  - Then 4-8 bars more of A without bass, and A fades out by the next phrase boundary.
- **Pitfalls:**
  - swapping mid-phrase
  - swapping too late, which leaves a long, thin drums-only stretch
  - a **gap** between basslines, which sounds hollow (Digital DJ Pool)
  - both basslines at full, which sounds muddy
  - clashing keys under the swap

### 7.3 Three-band EQ swap (full choreography)
- **When:** busy tracks where both have content throughout. Gives the most "invisible" blends.
- **Length:** 16-32 bars. Each band hands over on its own phrase or half-phrase boundary.
- **Automation (32 bars), "highs first, mids in the middle, bass at the switch":**
  - Bar 0: B in: fader 1.0, low 0, mid 0.3, high 0.
  - Bars 0-8: B.high 0→1, A.high 1→0.5. B's hats replace A's.
  - Bars 8-16: B.mid 0.3→1, A.mid 1→0.6.
  - **Bar 16: bass switch** (A.low→0, B.low→1 within 1 beat). A.high→0 at the same time.
  - Bars 16-24: A.mid 0.6→0.
  - Bars 24-32: A.fader→0, out on bar 32.
- **Rule:** at every moment, at most one track has full low, and the two tracks' gains in each band sum to no more than about 1.0-1.2.

### 7.4 Filter sweep / filter fade
- **When:** busy tracks, or tracks with filtered sections of their own ("complement" what the producer did; Digital DJ Tips). Also hides small key or groove differences. House, French house, disco, tech house.
- **Length:** 8-16 bars. Ends on a phrase boundary.
- **Automation (16 bars, Native Instruments' "filter fade"):**
  - Before bar 0: B's filter is a high-pass, fully clockwise, so no lows.
  - Bars 0-16: B.fader up over bars 0-4. B's HPF sweeps from fully on back to neutral over bars 0-16. A's low-pass sweeps from neutral to fully closed over bars 4-16.
  - Bar 16: A.fader→0. Both filters return to neutral (A's after it is muted).
  - Variant: do A's HPF sweep over the last 8 bars of a breakdown, then cut to B on the downbeat.
- **Pitfalls:** a filter sweep every 8 bars or every transition (an "instant beginner tell", Digital DJ Pool), leaving a filter half-engaged after the transition, the same sweep in the same style throughout the set (DJ TechTools).

### 7.5 Echo out / delay throw
- **When:** exits without a matching outro; big BPM or genre changes; hip-hop, open format, pop, weddings; clean exits from vocal tracks. Works without beatmatching.
- **Length:** the effect lasts 1 bar. The tail rings for about 1-2 bars under B.
- **Automation:**
  1. Set a beat-synced echo or delay: ½ or ¾ beat works almost anywhere, or 1 beat. Feedback is medium.
  2. On the **last beat of A's phrase** (or the last word of a vocal line), engage the echo, then pull A's fader to 0 within 1 beat (the echo is post-fader or "trails on", so the tail continues).
  3. Start B on the **next downbeat**, either dry or under the decaying tail.
  4. Turn echo feedback down within 2 bars so the tail doesn't wash over B.
- **Vocal variant:** echo the final word of a vocal phrase, cut A, and let the instrumental (or B) breathe for 8 bars (ZipDJ, acapella guide).
- **Pitfalls:** off-grid echo timing, a tail that smears over B's first phrase, using it every transition.

### 7.6 Cut / slam on the one
- **When:** hip-hop, DnB, open format, pop, big room. Big BPM changes. When the next track should arrive with impact. When two tracks would clash if layered.
- **Length:** instant (0 bars of overlap).
- **Automation:**
  1. Count A's phrase. At the end of a verse, hook or chorus, or where A's big elements are dropping out, pick the downbeat that would start A's next phrase.
  2. On that downbeat, B starts from a phrase-start cue (ideally a strong section) at full volume, and A goes to 0 at the same instant.
  3. Optional: a 1-beat spinback or brake on A's last beat (see 7.9).
- **Rules:** always on a downbeat, always at a phrase boundary, never mid-sentence (DJ Record Pool). Timing matters, not fader speed: the next downbeat of A is *replaced* by B's first downbeat.
- **Pitfalls:** cutting into a weak, quiet section of B; cutting A mid-phrase; forgetting the fader.

### 7.7 Loop roll / loop tightening
- **When:** EDM, big room, DnB, open format. Builds tension into a drop, or exits from a track that has no outro.
- **Length:** 4-8 bars.
- **Automation (8 bars):**
  - Bars 0-4: loop the last 4 beats of A's phrase (a 1-bar loop).
  - Bars 4-6: halve to 2 beats.
  - Bar 6: 1 beat.
  - Bar 7, beats 1-2: ½ beat.
  - Bar 7, beats 3-4: ¼ beat. Optional HPF sweep and reverb or echo rising over bars 4-8.
  - **Bar 8 downbeat:** cut A (or throw it into an echo out) and slam B in on its drop or phrase start (We Are Crossfader; VibesDJ).
- **Pitfalls:** loops that don't halve on the beat; using rolls repeatedly ("roll/beatmasher used the same way all set", DJ TechTools); a roll into a weak section.

### 7.8 Acapella over instrumental
- **When:** creating a live mashup moment. Hip-hop or pop vocals over a house or club instrumental. Extending a hook.
- **Requirements:**
  - Tempo matched, with the vocal stretched ≤6-8% (beyond that it sounds chipmunk-like or sluggish). Push the instrumental's tempo before the vocal's.
  - Keys same or ±1 Camelot, or pitch-shift by 1-2 semitones at most. Confirm by ear, since acapella key detection is unreliable.
  - Choose the instrumental to fit the vocal.
- **Length:** usually one hook (8 bars) or one verse (16 bars).
- **Automation:**
  1. Start the vocal on a clear structural point of the instrumental: a breakdown, a drop, or a phrase start.
  2. Align the vocal's first strong syllable or downbeat to bar 1 (many vocals have pickups that start before the downbeat).
  3. Cut the instrumental's mids slightly (roughly the 200 Hz-4 kHz region) while the vocal plays.
  4. Exit by echoing the final word, then let the instrumental run 8 bars.
- **Pitfalls:** an acapella on top of a track that already has vocals, vocal phrases out of sync with the instrumental's phrasing, level mismatch between sources.

### 7.9 Power-down / brake / spinback
- **When:** open format, hip-hop, dancehall, throwbacks, big BPM jumps, theatrical moments. Wrong in a smooth house or techno journey unless breaking the flow is the point.
- **Length:** about 1 beat. Brake set to about 1 beat, sometimes with a ½-beat echo.
- **Automation:** count to the end of A's phrase. On the **final beat** (some DJs start on beat 3 of the last bar), trigger the brake or spinback. Close A before the effect turns to noise. Drop B on the next "one".
- **Budget:** at most once or twice per set. If every transition is a stop or spinback, people conclude you can't mix (DJing Tips; VibesDJ).

### 7.10 Drop swap / double drop
- **When:** DnB (signature move), dubstep, big room, bass music. Peak moments only.
- **Drop swap** (B replaces A's drop):
  1. During A's breakdown, bring B in from a cue placed the same number of bars before B's drop as A's breakdown has bars left (e.g. both 16 bars before the drop).
  2. B rides under A with B.low = 0.
  3. On the drop downbeat, cut A entirely (or A.low→0 and A.fader→0), and bring B to full with low = 1. The crowd expects A's drop and gets B's.
- **Double drop** (both drops together; Vande Veire template):
  1. Cue both 16 bars before their drops. B fades in over 16 bars with B.low = 0.
  2. Both drops land on the same downbeat.
  3. After 8-16 bars of combined drop, swap bass (B.low→1, A.low→0) on a phrase boundary.
  4. A fades out over a total of 32 bars from the start.
- **Rules:** keys should be compatible (the overlap is fully melodic); never two full bass drops at full low EQ; never two double drops in a row, and not right after a rolling layered transition (Vande Veire's state machine forbids it).
- **Budget:** a few per hour at most. They are climaxes, not filler.

### 7.11 Other recipes worth keeping
- **Single-phrase beatmix:**
  1. Start B in headphones one phrase before the mix point.
  2. Bring it in over a drum-dominated section of both tracks.
  3. Play both together for 4, 8 or sometimes 16 bars.
  4. Exit A in one move on a downbeat, or with a short fade.
  Good default when tracks lack long DJ intros (Digital DJ Tips).
- **End-to-end:** A has a clean ending. B starts on the downbeat that matches A's final downbeat, at full volume, with an energetic opening. If A ends off-phrase, start B on the next bar's 1, even if that leaves a short silence (Digital DJ Tips). Common for radio edits and pop.
- **Fade ("get out of jail"):**
  1. Pick a fade point (a chorus, or a chorus after a chorus).
  2. Drop A sharply at first, then fade over 10-15 s, finishing near the end of the current 8-bar phrase.
  3. Start B on a phrase downbeat.
  Use it to escape a track that isn't working or to cross genres.
- **Rolling (DnB):** A's last 32 bars before its drop ends, overlapped with B's 16-bar build so that B's drop continues A's energy. Fade-in and fade-out 16 bars each (Vande Veire).
- **Relaxed:** A exits 16 bars before its high→low boundary into B's intro. Fade-in and fade-out 16 bars each. Gives the floor a rest.

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

## 9. Verifiable rules (machine-checkable rewards)

**Assumed plan representation:**
- For each track i: native BPM_i, played BPM_i(t), beat and downbeat grid with confidence, phrase grid (bar index from the track's first downbeat, corrected by phrase-offset detection), sections with labels and energy, vocal-presence per bar, Camelot key with confidence, energy level 1-10, and a style embedding.
- For each transition k: transition type; start bar T_k; switch bar S_k; end bar E_k; per-deck automation curves for fader, low, mid and high (linear 0..1); FX events (type, start, end, sync value); tempo ramp.

**Scoring:**
- **[H]** = hard constraint. A violation is a large penalty or rejection.
- **[S]** = soft. Score proportionally.
- "Phrase boundary" = bar index ≡ 0 (mod 8) in that track's phrase grid, or a detected section boundary. For tracks whose detected period is 4 bars, mod 4 is accepted.

### A. Timing and structure
- **R1 [H] Phrase-aligned entry.** B's first audible downbeat (B.fader × max band gain > 0.05) falls on a phrase boundary in A's grid **and** at a phrase boundary or section start in B. Tolerance: ±1 audio frame (≤ 20 ms) from the downbeat.
  *Justification:* DJ TechTools / DJKit phrase locking; Zehren Rule 2 (switch points always on the downbeat that starts a 4-bar period); Spotify restricts transition points to downbeats (Bittner 2017).
- **R2 [H] Phrase-aligned switch.** The switch bar S_k (bass handover, or the point where B dominates) is a phrase boundary in **both** tracks.
  *Justification:* Digital DJ Tips (swap on a "one"); Home DJ Studio (never drop a bassline mid-phrase); Zehren Rule 2.
- **R3 [H] Phrase-aligned exit.** A's last audible bar ends on a phrase boundary or section end in A (cut, echo-out tails excepted, ≤2 bars).
  *Justification:* Digital DJ Tips (finish fades by the end of the 8-bar phrase); DJ Record Pool (cut at phrase boundaries, never mid-sentence).
- **R4 [H] Transition length quantized.** The overlap length (E_k − T_k) in bars is in {0 (cut), 1-2 (echo/brake tail), 4, 8, 12, 16, 24, 32, 48, 64, 96, 128}, i.e. a multiple of 4 bars once it exceeds 2 bars.
  *Justification:* transition-length histogram peaks every 32 beats in 20,765 real transitions (Kim 2020); Vande Veire's 16- and 32-bar fades.
- **R5 [S] Genre-appropriate length.** Median overlap per set, in bars: house/techno 16-64; progressive/melodic 32-64+; EDM/big room 8-16; DnB 16-32; hip-hop/open format/pop 0-8. Score 1.0 inside the band, decaying linearly to 0 at ½× or 2× the band edges.
  *Justification:* EDM Ghost Production genre guide; Vande Veire; Native Instruments; CMUSE; Mixgraph.
- **R6 [S] Entry and exit zones.** For blend-type transitions, B's entry point lies within the first 20% of B (or at its intro, build or breakdown start), and A's exit lies within the last 25% of A (or at its outro or breakdown). Exempt: power-block, drop swap, hip-hop quick mixes.
  *Justification:* Spotify's transition-point pruning rules (Bittner 2017).
- **R7 [S] Salient takeover.** The section of B starting at S_k has mean energy ≥ 0.4 × B's maximum section energy, unless the transition type is "relaxed" or "reset".
  *Justification:* Zehren Rule 3 (salience), implemented as a 0.4 × max harmonic-energy threshold over the 4 bars after the switch.
- **R8 [H] Drop alignment.** If the type is double drop or drop swap, B's drop downbeat coincides with A's drop downbeat (or A's would-be drop) with 0 beat offset, and both tracks' cues are the same number of bars (8, 16 or 32) before their drops.
  *Justification:* double-drop technique (DJ Gear 2K; Home Music Maker; Vande Veire).
- **R9 [S] Let tracks breathe.** Each track's audible solo time (not overlapped) is at least: house/techno 90 s; progressive 120 s; EDM/DnB 45 s; hip-hop/open format 30 s; pop/wedding 60 s. And every track plays at least one complete core section (chorus or drop) unless the type is "rescue fade".
  *Justification:* Digital DJ Tips ("don't cut tracks off before they finish their section"); DJ TechTools ("don't rush if people are enjoying it"); tracks-per-hour tables (VibesDJ, Mixgraph). The exact seconds are heuristics derived from those tables.

### B. Low end and spectral clarity
- **R10 [H] One bassline.** At every moment, A.fader·A.low + B.fader·B.low ≤ 1.1. Both terms ≥ 0.5 at once for ≤ 1 beat, except over a bass crossover of ≤ 2 bars where neither track's bassline is in a "full bass" section, or in an explicitly flagged bass-alternation effect.
  *Justification:* Vande Veire's crossfade (bass of only one song at any moment); Digital DJ Tips bass swap; mistake lists naming bass clash as the clearest amateur tell.
- **R11 [S] No bass gap.** Around the switch, max(A.fader·A.low, B.fader·B.low) ≥ 0.7 at all times, unless the musical content itself has no bass (breakdown or drum intro) or a deliberate breakdown-style drop is planned.
  *Justification:* Digital DJ Pool (a hollow mix means you left a gap between basslines).
- **R12 [S] High-band sum.** The sum of high-band contributions is ≤ 1.3 for no more than 8 consecutive bars.
  *Justification:* doubled hats and harshness. Practitioner convention (the 3-band choreography in Digital DJ Pool / Home DJ Studio).
- **R13 [H] No boost.** Every EQ and fader gain is ≤ 1.0 (unity). The master never clips (true peak ≤ −1 dBTP after summing).
  *Justification:* DJ TechTools, never boost EQ past 12 o'clock.
- **R14 [S] Loudness continuity.** Short-term loudness (3 s window, LUFS) across the transition stays within −3 dB / +2 dB of the mean of A's solo loudness in the 8 bars before T_k and B's solo loudness in the 8 bars after E_k. Exempt: deliberate breakdowns and cuts into a quiet intro.
  *Justification:* real DJ mixes keep relatively constant energy through transitions (Kim, Yang & Nam DAFx 2022); Vande Veire normalizes ReplayGain. The dB thresholds are heuristics.
- **R15 [S] Human-like control movement.** Per deck, at most 2 controls change in any 4-second window (two hands). Curves are monotonic during the transition (A's gains non-increasing, B's non-decreasing), except FX and filter returns after mute.
  *Justification:* Kim, Yang & Nam's synthetic-data model of realistic DJ control (one gain per hand per 4 s; monotonic curves).

### C. Vocals and harmony
- **R16 [H] Vocal overlap.** The number of bars where both tracks have vocal presence and are audible (fader × mid > 0.3) is ≤ 1 bar per transition (score 1.0). 2 bars gets a penalty. Above 2 bars is a hard fail. Exempt: an explicit acapella-over-instrumental type where the instrumental has no vocal.
  *Justification:* Vande Veire tolerates exactly a 1-bar vocal overlap and treats 2 or more as a clash; Digital DJ Tips calls two vocals a "no-no"; 6.5% of bad auto-transitions in Spotify's test were "transitioning mid-vocals".
- **R17 [H] No mid-sentence exits.** A's last vocal bar before an exit, cut or echo must end at a vocal-phrase end. Operationally: A is not cut or muted during a bar flagged vocal unless that bar is the last vocal bar of a contiguous vocal run (an echo on the last word is allowed).
  *Justification:* DJ Record Pool ("never cut mid-sentence").
- **R18 [S] Harmonic compatibility under melodic overlap.** Let melodic overlap = bars where both tracks are audible with mid gain > 0.5 and neither is in a drums-only section. If melodic overlap ≥ 4 bars:
  - Camelot relation ∈ {same, ±1 same letter, same number letter swap} scores 1.0
  - diagonal (±1 and letter swap) scores 0.7
  - +2 same letter scores 0.8 only if flagged as an energy boost
  - +7 same letter scores 0.6 only if flagged and the overlap is mostly percussive
  - anything else scores 0
  If melodic overlap < 4 bars, the score is 1.0 regardless of key.
  *Justification:* Mixed In Key Camelot rules and energy boost; Vande Veire's allowed keys; Digital DJ Tips / Digital DJ Pool (key only matters when melodies overlap).
- **R19 [S] Energy boost budget.** Flagged +2 or +7 key boosts occur at most once per 20 minutes and never in consecutive transitions.
  *Justification:* MIK (every 20-30 minutes, not all the time).
- **R20 [S] Key confidence gate.** If either key confidence is low (< 0.6, or two analyzers disagree), melodic overlap is ≤ 8 bars.
  *Justification:* key detection accuracy of 41-86% (Digital DJ Pool); "probabilities, not guarantees".
- **R21 [S] Transposition sparingly.** Pitch-shifting a track (key change without tempo change) is ≤ ±1 semitone, applied to ≤ 5% of tracks in a set.
  *Justification:* in real mixes only 2.5% of tracks are transposed, 94.3% of those by 1 semitone (Kim 2020); Vande Veire limits pitch-shifts to ±1 semitone.

### D. Tempo and grid
- **R22 [H] Stretch limit.** For every track, played/native tempo ratio r (after octave normalization) satisfies 0.95 ≤ r ≤ 1.06 for normal play. Allowed: 0.92 ≤ r ≤ 1.08 only while the track is masked (fader < 0.5, or in a breakdown or FX wash). Score 1.0 for |r−1| ≤ 0.03, linear down to 0.5 at the normal limits.
  *Justification:* 86.1% of real tracks are within ±5% (Kim 2020); Ishizaki's 0.90-1.10 "strict" band, with slow-down more objectionable; key-lock artifacts noticeable beyond about 5-6% and obvious beyond about 8% (practitioner reports).
- **R23 [S] Split the stretch.** When native BPMs differ by d% > 3%, the stretch is shared so neither track exceeds about 0.6·d% (e.g. A ramps up, B starts slowed and ramps back toward native).
  *Justification:* Ishizaki's optimal tempo adjustment (stretching both tracks in opposite directions lowers measured discomfort).
- **R24 [S] Tempo ramp smoothness.** Master tempo changes ≤ 0.5% per bar and only during transitions or over ≥ 8 bars. No direction reversal within 3 consecutive transitions unless an energy reset is flagged.
  *Justification:* Spotify ramps tempo gradually across the transition beats (Bittner 2017); Ishizaki adds gradual ramp periods. The 0.5%/bar figure is a heuristic.
- **R25 [H] Tempo-independent methods for big gaps.** If native BPMs differ by more than 8% and are not within ±3% of a 2:1 or 1:2 ratio, the transition type is in {cut, echo out, brake/spinback, fade/end-to-end}, with audible overlap ≤ 2 bars of rhythmic content.
  *Justification:* VibesDJ (>8% → tempo-independent methods); Mixxx AutoDJ (sync only within 6%).
- **R26 [H] Grid confidence for blends.** Overlaps longer than 2 bars with both kicks audible require both tracks' beat and downbeat confidence ≥ 0.8 and predicted onset drift ≤ 10 ms across the overlap. Downbeats must coincide (bar phase offset = 0).
  *Justification:* beat misalignment was the top failure in Spotify's curator test (15.2%); Ishizaki's strong/weak beat mismatch finding; Zehren's warning about confusing beat 1 and beat 3. The 10 ms figure is a heuristic.

### E. Programming and variety
- **R27 [S] Transition variety.** No transition type is used 3 or more times in a row. In sets with ≥10 transitions, no single type is used for > 50% of transitions (techno/progressive: > 70%, but then R28 must pass). Double drops never in consecutive transitions and never directly after a rolling/layered transition.
  *Justification:* Vande Veire's state machine (prevents repeating types; forbids double drop after rolling or double drop); DJ TechTools on repetitive effects.
- **R28 [S] Length and curve variety.** Within each hour, at least 3 distinct overlap lengths are used, and the coefficient of variation of overlap lengths is ≥ 0.25 (relaxed to ≥ 0.15 for techno and progressive). Switch timing varies (switch at ¼, ½ or ¾ of the overlap, not always the midpoint).
  *Justification:* anti-template heuristic derived from "same transition every time" being a top tell; Vande Veire's asymmetric fades (16 in, 32 out for double drops).
- **R29 [S] FX budget.**
  - Any FX (filter sweep, echo, reverb, roll) in ≤ 40% of transitions.
  - FX active ≤ 15% of total set time.
  - The same FX in ≤ 2 consecutive transitions.
  - Brake/spinback ≤ 2 per set.
  - Loop rolls ≤ 1 per 20 minutes.
  - All delay and echo times beat-synced (¼, ½, ¾, 1 or 2 beats).
  - Every filter returns to neutral within 1 bar after the transition ends.
  *Justification:* Digital DJ Pool, DJ TechTools, DJs On Demand on overusing FX; DJing Tips (brakes once or twice per set). The percentages are heuristics.
- **R30 [S] Energy step.** |E_{i+1} − E_i| ≤ 1 for ≥ 80% of transitions. Steps of ≥3 occur at most once per 30 minutes and only when flagged as a reset or genre change.
  *Justification:* Mixed In Key ("same energy or one number apart"; energy jumps can feel too sudden even when keys match).
- **R31 [S] Arc shape (by slot).**
  - Opening slot: energy ≤ 5 for the first 25% and max energy ≤ 7.
  - Peak slot: max energy reached in the last 50%.
  - Full night: the smoothed energy curve has its global max between 55% and 90% of the set, with at least one dip of ≥2 levels after the first 30% (a breather) and a non-zero downward slope in the last 10% if closing.
  - Penalize a monotonic curve over > 40 minutes.
  *Justification:* Vande Veire (build, climax, rest, second climax); RA (openers stay restrained); DJ TechTools (pacing; save bangers for the end); Digital DJ Tips (tension and release). The percentages are heuristics.
- **R32 [S] Hit density.** No more than 3 consecutive tracks at energy ≥ 8 (or flagged "weapon/anthem"), then a track of energy ≤ 7. Anthems are not all in the first 30% of the set.
  *Justification:* DJ TechTools ("don't play all the best tracks first"); MIK (insert a low-energy moment after several bangers).
- **R33 [S] Style coherence.** The distance between consecutive tracks' style embeddings is ≤ the 50th percentile of pairwise library distances, and all tracks are within the nearest 25% of the library to the set's style centroid. Deliberate genre switches are allowed ≤ 1 per 30 minutes and must use a short transition type (≤ 8 bars overlap).
  *Justification:* professional mixes stay in a small style neighbourhood; Vande Veire uses the closest quarter of the library to the first track and a centroid weight of 0.4.
- **R34 [S] Tempo continuity across the set.** Consecutive native tempos within ±6% (or a 2:1 relation). Total set tempo drift in the warm-up phase ≤ +6 BPM per hour (house/techno). *Practitioner heuristic.*
  *Justification:* Kim 2020 tempo distribution; DJ TechTools pacing; RA (openers stay slow).
- **R35 [S] Tracks per hour within genre band** (§2.4 table).
  *Justification:* Kim 2020 average (~15.5 tracks per hour of mix); Mixgraph / VibesDJ.
- **R36 [H] No repeats.** No track is played twice in a set. The same artist is not in consecutive slots unless it's a deliberate block. *Practitioner convention.*
- **R37 [S] Vocal/instrumental alternation.** No more than 3 consecutive vocal-dominant tracks (vocal presence in > 40% of bars).
  *Justification:* Digital DJ Tips (alternate vocal and instrumental).

### F. Recipe conformance (per transition type)
- **R38 [H] Cut:** overlap = 0 bars (≤ 1 beat for a brake/spinback tail). B starts at full on a phrase-start downbeat. B's entry section passes R7.
- **R39 [H] Echo out:** echo engaged on the last 1-2 beats of A's phrase. A.fader → 0 within 1 beat after engagement. Tail ≤ 2 bars. B starts on the next downbeat or within 1 bar.
- **R40 [H] Bass swap:** B.low = 0 from T_k until S_k. A.low = 0 from S_k (±1 beat) on. The swap completes within ≤ 2 bars.
- **R41 [H] Filter sweep:** sweep length ≥ 4 bars, ends on a phrase boundary, filters at neutral when the transition ends.
- **R42 [H] Loop roll:** loop lengths halve only on beat boundaries (4 → 2 → 1 → ½ → ¼ beats). The last loop ends exactly on the downbeat where B enters.
- **R43 [H] Double drop / drop swap:** R8 holds. At most one track has low > 0.5 during the combined drop. Not in consecutive transitions.

### Suggested aggregate score
`score = 100 × (Π over hard rules of pass_i) × (Σ_j w_j·s_j / Σ_j w_j)`

Suggested weights for the soft rules:

| Weight | Rules | Theme |
|---|---|---|
| 3 | R14, R16-adjacent penalties, R18, R26-adjacent penalties | audible clarity |
| 2 | R5, R7, R22-score, R27, R28, R29, R30, R31, R33 | taste and variety |
| 1 | everything else | |

Report every violated rule with its timestamp so the planner can repair locally.

---

## 10. Listening rubric (for an LLM judging rendered audio)

Listen to the full transition plus about 16 bars before and after. Score each axis 1-10 using the anchors. Then apply the caps.

| # | Axis | 1-2 (bad) | 5-6 (passable) | 9-10 (excellent) |
|---|---|---|---|---|
| 1 | **Beat sync** | Kicks flam or gallop, drift audible, downbeat on beat 3 | Locked mostly, brief smear | Kicks fuse into one; sounds like one record |
| 2 | **Phrase / structure fit** | Enters or exits mid-phrase; lurches; cuts a vocal mid-line | On phrase but the moment feels arbitrary | Every change lands where the music wanted it; B takes over on a salient section |
| 3 | **Low-end management** | Two basslines fighting, boomy mud, or a hollow gap | Brief bass overlap or thin moment | One clean bassline throughout; the swap is felt, not heard |
| 4 | **Harmonic compatibility** | Sour clash over melody or vocal | Mild tension, short | Melodies agree, or overlap avoided so key is irrelevant; boosts feel intentional |
| 5 | **Vocal handling** | Two vocals talk over each other; vocal chopped mid-word | Brief overlap or slightly awkward exit | Vocals hand off cleanly, or an echo on the last word |
| 6 | **Level / energy continuity** | Volume hole or jump; energy collapses at the switch | Small dip or bump | Perceived loudness and drive constant (or changes on purpose at a drop) |
| 7 | **Spectral clarity** | Harsh doubled hats, smeared mids, clipping | Somewhat busy | Every element distinct; the mix breathes |
| 8 | **Transition choice and length** | Wrong tool (long blend of clashing tracks, 64-bar layering of vocal pop, spinback in a deep set) | Acceptable, generic | The obvious-in-hindsight choice for this pair and moment |
| 9 | **FX taste** | FX as decoration, off-grid echoes, filter left on, cheesy samples | Slightly heavy-handed | FX absent or invisible-yet-helpful; complements the track's own production |
| 10 | **Selection fit** | Groove, timbre, era or mood mismatch; "why this track?" | Compatible but unremarkable | B feels like the inevitable next chapter; lifts or turns the story |
| 11 | **Human feel** | Mechanical: linear symmetric fade, template-like, robotic precision with no intent | Competent but predictable | Sounds like a skilled person made a decision; small asymmetries with a purpose |
| 12 | **Dance-floor effect** | Would clear the floor or confuse dancers | Keeps people moving | Would make people react (hands up, shouts) or deepen the trance |

**Caps (apply after scoring):**
- Audible flam or beat drift longer than 1 bar → overall ≤ 3.
- Two full basslines clashing for more than 1 bar → overall ≤ 4.
- Two lead vocals overlapping for more than 2 bars → overall ≤ 4.
- An entry or exit clearly mid-phrase in phrase-driven genres → overall ≤ 5.
- Clipping or distortion → overall ≤ 4.
- Stretch artifacts (chipmunk, warble, smeared transients) clearly audible → axis 7 ≤ 4.

**Overall score:**
`overall = 0.15·sync + 0.12·phrase + 0.12·low-end + 0.08·harmony + 0.08·vocals + 0.08·level + 0.06·clarity + 0.08·choice + 0.05·FX + 0.08·selection + 0.07·human + 0.03·floor`

Then apply the caps.

**Questions the critic should answer in text:**
1. At what time (and bar) did B become the dominant track? Did it feel like a natural boundary?
2. Was there ever a moment with no clear lead track, or two lead tracks?
3. Name the single biggest flaw and the bar where it happens.
4. Would an experienced DJ in this genre have chosen this transition type and length? If not, what would they have done?
5. Does this transition sound like the others in the set (template smell)?

---

## Sources (consolidated)

**Academic / measured**
- Kim, Choi, Sacks, Yang, Nam. "A Computational Analysis of Real-World DJ Mixes using Mix-To-Track Subsequence Alignment." ISMIR 2020. https://arxiv.org/abs/2008.10267 ; https://archives.ismir.net/ismir2020/paper/000352.pdf
- Kim, Yang, Nam. "Reverse-Engineering the Transition Regions of Real-World DJ Mixes using Sub-band Analysis with Convex Optimization." NIME 2021. https://nime.pubpub.org/pub/g7avj1a7 ; code https://github.com/mir-aidj/transition-analysis
- Kim, Yang, Nam. "Joint Estimation of Fader and Equalizer Gains of DJ Mixers Using Convex Optimization." DAFx 2022. https://mac.kaist.ac.kr/pubs/KimYangNam-dafx2022.pdf
- Kim et al. "Raveform: A Dataset of Metrical and Functional Structure Annotations for EDM Tracks in DJ Mixes." TISMIR. https://transactions.ismir.net/articles/10.5334/tismir.288
- Vande Veire, De Bie. "From raw audio to a seamless mix: creating an automated DJ system for Drum and Bass." EURASIP J. Audio, Speech, Music Proc. 2018:13. https://asmp-eurasipjournals.springeropen.com/articles/10.1186/s13636-018-0134-8 ; code https://github.com/aida-ugent/dnb-autodj
- Zehren, Alunno, Bientinesi. "Automatic Detection of Cue Points for DJ Mixing." arXiv 2007.08411 (2020); Computer Music Journal 46(3), 2022. https://arxiv.org/abs/2007.08411 ; https://doi.org/10.1162/comj_a_00652
- Bittner et al. (Spotify). "Automatic Playlist Sequencing and Transitions." ISMIR 2017. https://archives.ismir.net/ismir2017/paper/000086.pdf
- Ishizaki, Hoashi, Takishima. "Full-Automatic DJ Mixing System with Optimal Tempo Adjustment based on Measurement Function of User Discomfort." ISMIR 2009. https://archives.ismir.net/ismir2009/paper/000043.pdf
- Chen et al. "Automatic DJ Transitions with Differentiable Audio Effects and Generative Adversarial Networks." ICASSP 2022. https://arxiv.org/abs/2110.06525

**Books / vendors / education**
- Brewster & Broughton. *How to DJ Right: The Art and Science of Playing Records.* Grove Press, 2003. https://groveatlantic.com/book/how-to-dj-right/ (description only; cited second-hand via Vande Veire & De Bie)
- Mixed In Key: Camelot wheel, energy boost, energy level and advanced technique pages (URLs in §2 and §6)
- Pioneer DJ / rekordbox: Phrase Edit operation guide; "How to read a crowd" (URLs in §1 and §4)
- Native Instruments blog: "5 basic DJ transitions" https://blog.native-instruments.com/dj-transitions/
- Resident Advisor: "The esoteric art of the opening DJ" https://ra.co/features/1095

**Practitioner sites**
- Digital DJ Tips: five basic transitions, house mixing guide, acapellas, "what song to play next"
- DJ TechTools: phrasing 101, phrase mixing, bad habits, reading the dance floor, forum threads
- Digital DJ Pool, Home DJ Studio, VibesDJ, Mixgraph, OpenKeyScan, Setflow, Djoid, TrackScore, EDM Ghost Production, DJ.Studio, We Are Crossfader, beatif.studio, DJ Record Pool, CMUSE, DJing Tips, ZipDJ, DJs On Demand, The DJ Revolution, Club Ready DJ School, The Ghost Production, DJ Gear 2K, Home Music Maker, Benztown (Danny Byrd), Lunarkal, DJ Raj, SoDJLA, DJ Lou Paris, DJKit, Mixxx wiki, Pioneer DJ and VirtualDJ forums

(URLs for each are given in the section where they are used.)
