<script setup lang="ts">
import { computed, nextTick, onMounted, reactive, ref, watch } from "vue"
import { DitherBadge, DitherButton, DitherConsole, DitherGridScan, DitherKnob, DitherMeter, DitherSlider, DitherSpinner } from "@dither-kit"
import Deck from "./Deck.vue"
import { drawWave, fmt } from "./wave"

// ---------- state
const S = reactive({ lib: [] as any[], A: null as any, B: null as any, set: [] as any[], mix: null as any,
  busy: false, status: "idle, waiting for records", say: "evening. load two records into the decks, or hand me a set list.",
  log: [] as { text: string; level?: "info" | "success" | "warn" | "error"; at?: string }[], q: "", brief: "",
  t: 0, playing: false, level: 0, xf: 50, rated: 0 })
const api = async (path: string, opts?: RequestInit) => { const r = await fetch(path, opts); if (!r.ok) throw new Error((await r.text()) || String(r.status)); return r.json() }
const log = (text: string, level: "info" | "success" | "warn" | "error" = "info") =>
  S.log.push({ text, level, at: new Date().toLocaleTimeString().slice(0, 5) })
const busy = (on: boolean, msg?: string) => { S.busy = on; S.status = msg || (on ? "working" : "idle") }

// ---------- the moth: pixel mascot wearing headphones
const MOTH = ["....a......a....", ".....a....a.....", "......a..a......", ".....hhhhhh.....", "....h.bbbb.h....",
  "LLLhhbeebbhhRRRR", "LLLLPbbbbbbPRRRR", "LLLLPbbbbbbPRRRR", ".LLLLhbbbbhRRRR.", "..LLL.bbbb.RRR..", "...LL.bbbb.RR...",
  ".....l.bb.r.....", "......bbbb......", ".......bb......."]
const MC: Record<string, string> = { a: "#8d857a", h: "#ece7dc", P: "#ffb000", b: "#ece7dc", e: "#0b0a09", L: "#ffb000", R: "#ffb000", l: "#8d857a", r: "#8d857a" }
const moth = { L: [] as string[], R: [] as string[], body: [] as string[] }
MOTH.forEach((row, y) => [...row].forEach((c, x) => {
  if (c === ".") return
  const fill = (c === "L" || c === "R") && (x + y) % 2 ? "#c78900" : MC[c]
  ;(c === "L" ? moth.L : c === "R" ? moth.R : moth.body).push(`<rect x="${x}" y="${y}" width="1" height="1" fill="${fill}"/>`)
}))
const mothSvg = `<g class="wing wl">${moth.L.join("")}</g><g class="wing wr">${moth.R.join("")}</g>${moth.body.join("")}`

// ---------- library
async function loadLib() { S.lib = await api("/api/library?q=" + encodeURIComponent(S.q)) }
let qt = 0
watch(() => S.q, () => { clearTimeout(qt); qt = window.setTimeout(loadLib, 200) })
const byId = (id: string) => S.lib.find(t => t.id === id)
function addSet(t: any) { if (!S.set.find(s => s.id === t.id)) S.set.push(t) }
async function analyzeFile(f: string) { watchJob(await api("/api/analyze/" + encodeURIComponent(f), { method: "POST" }), "analyzing + listening") }
const over = ref(false)
async function upload(files: FileList | null | undefined) {
  if (!files?.length) return
  const fd = new FormData(); [...files].forEach(f => fd.append("files", f))
  log(`uploading ${files.length} file(s)`)
  watchJob(await api("/api/upload", { method: "POST", body: fd }), "dissecting new records")
  loadLib()
}

// ---------- jobs
async function watchJob(job: any, label: string) {
  busy(true, label); let seen = 0, previewed = false, queued = false
  while (true) {
    await new Promise(r => setTimeout(r, 2000))
    const j = await api("/api/jobs/" + job.id)
    if (j.status === "queued" && !queued) { queued = true; log("queued: another job has the decks, i'll start when it's done", "warn"); busy(true, "queued behind another job") }
    if (j.preview && !previewed) { previewed = true; showMix(j.preview); log("quick take ready, press play", "success") }
    j.events.slice(seen).forEach((ev: any) => { if (ev.msg) { log(ev.msg); S.say = ev.msg + "…"; busy(true, ev.msg) } }); seen = j.events.length
    if (j.status === "done") { busy(false, "idle"); loadLib(); return j.result }
    if (j.status === "error") { busy(false, "error"); log(j.error, "error"); S.say = "that one went sideways: " + j.error; return null }
  }
}
async function startMix(ids: string[], takeover: boolean) {
  if (S.busy) return  // the disabled attr lands a tick late; a fast double click gets here twice
  const brief = S.brief.trim()
  S.say = takeover ? "alright, i've got the booth. give me a few minutes to dig through these." : "nice pair. let me listen to both properly first."
  log(`mix requested: ${ids.length} tracks${brief ? ` — "${brief}"` : ""}`)
  busy(true, "sending to the booth")  // lock the button before the request returns: no double jobs
  const r = await watchJob(await api("/api/mix", { method: "POST", headers: { "content-type": "application/json" },
    body: JSON.stringify({ ids, brief, takeover }) }), "mixing")
  if (r) { showMix(r); S.say = r.story }
}
const canPerform = computed(() => S.A && S.B && S.A.id !== S.B.id && !S.busy)

// ---------- the loaded routine
const audio = ref<HTMLAudioElement | null>(null)
const m = computed(() => S.mix?.mix)
const isRoutine = computed(() => !!m.value?.lanes)
function showMix(r: any) {
  S.mix = r; S.rated = 0
  if (r.mix.decks) {  // routines name their decks: load them so the deck shows what MOTH played
    for (const [k, d] of Object.entries<any>(r.mix.decks)) { const t = byId(d.id); if (t) (S as any)[k] = t }
  }
  audio.value!.src = "/audio/mix/" + encodeURIComponent(r.mix.file)
  if (r.story) S.say = r.story
  nextTick(paint)
}
const liveLanes = computed(() => (m.value?.lanes || []).filter((l: any) => S.t >= l.start && S.t < l.end))
// a deck only shows the loaded mix when it holds the track that mix played (load a new record = clean deck)
const inMix = (side: string) => !!m.value?.decks && m.value.decks[side]?.id === (S as any)[side]?.id
const liveStems = (side: string) => !inMix(side) ? [] : liveLanes.value.filter((l: any) => l.deck === side)
  .flatMap((l: any) => l.stems?.length ? l.stems : ["vocals", "drums", "bass", "other"])
const deckLive = (side: string) => liveStems(side).length > 0
const critic = computed(() => S.mix?.critiques?.[0])
const scoreColor = (s?: number) => s == null ? "grey" : s >= 8 ? "green" : s >= 6.5 ? "orange" : "red"

// console knobs MOTH set for this take (read-only: the learning loop tunes them, not a mouse)
const KNOBS = [["vox_hp", "VOX HP", 20, 400], ["carve_db", "CARVE", 0, 12], ["room_send_vox", "ROOM", 0, .4], ["glue_gr_db", "GLUE", 0, 6]] as const
const knob = (k: string) => { const v = m.value?.knobs?.[k] ?? 0; return Number(v.toFixed(v >= 10 ? 0 : v >= 1 ? 1 : 2)) }

// ---------- transport + meters (Web Audio analyser on the mix)
let analyser: AnalyserNode | null = null, buf: Float32Array
function ensureAudioGraph() {
  if (analyser) return
  const ctx = new AudioContext(), src = ctx.createMediaElementSource(audio.value!)
  analyser = ctx.createAnalyser(); analyser.fftSize = 1024; buf = new Float32Array(analyser.fftSize)
  src.connect(analyser); analyser.connect(ctx.destination)
}
function togglePlay() { ensureAudioGraph(); audio.value!.paused ? audio.value!.play() : audio.value!.pause() }
function tick() {
  if (!audio.value) return
  S.t = audio.value.currentTime
  if (analyser) {
    analyser.getFloatTimeDomainData(buf)
    let s = 0; for (const v of buf) s += v * v
    const db = 20 * Math.log10(Math.sqrt(s / buf.length) + 1e-9)
    S.level = S.level * .6 + Math.max(0, Math.min(100, (db + 48) / 48 * 100)) * .4
  }
  const a = deckLive("A"), b = deckLive("B"), target = a && !b ? 0 : b && !a ? 100 : 50
  S.xf += (target - S.xf) * .15
  paint()
  if (S.playing) requestAnimationFrame(tick)
}
function onPlay() { S.playing = true; requestAnimationFrame(tick) }
function onPause() { S.playing = false; S.level = 0; paint() }
function seek(sec: number, play = false) { if (!m.value) return; audio.value!.currentTime = Math.max(0, sec); S.t = audio.value!.currentTime; if (play) { ensureAudioGraph(); audio.value!.play() } paint() }
const seekAt = (e: MouseEvent) => seek((e.offsetX / (e.target as HTMLElement).clientWidth) * m.value.duration)

async function rate(v: number) {
  if (!S.mix) return
  const note = prompt(v > 0 ? "what worked? (optional)" : "what's wrong with it? (MOTH reads this next time)") ?? ""
  await fetch("/api/rate", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ name: m.value.file, rating: v, note }) })
  S.rated = v
}

// ---------- the performance strip: waveform + 9 lanes (4 stems per deck + FX)
const waveC = ref<HTMLCanvasElement | null>(null), lanesC = ref<HTMLCanvasElement | null>(null)
const ROWS = ["A vocals", "A drums", "A bass", "A other", "B vocals", "B drums", "B bass", "B other", "FX"]
const MOVE_COL: Record<string, string> = { play: "#ffb000", loop: "#ff5a1f", roll: "#ff4d4d", chop: "#c6ff3d", riser: "#f5f1e6",
  impact: "#f5f1e6", gap: "#5d574f", tape_stop: "#8d857a", backspin: "#8d857a" }
function paint() {
  if (!waveC.value) return
  const mx = m.value
  if (!mx) return drawWave(waveC.value, null)
  const d = mx.duration, ph = S.t / d
  if (!mx.lanes) {
    drawWave(waveC.value, mx.waveform, { playhead: ph, regions: (mx.transitions || []).map((t: any) => ({ a: t.mix_start / d, b: t.mix_end / d, color: "rgba(198,255,61,.12)" })) })
    return
  }
  drawWave(waveC.value, mx.waveform, { playhead: ph })
  const cv = lanesC.value!, w = cv.width = cv.clientWidth, h = cv.height = cv.clientHeight, x = cv.getContext("2d")!
  const rh = h / ROWS.length
  x.font = "10px JetBrains Mono"; x.clearRect(0, 0, w, h)
  ROWS.forEach((r, i) => {
    x.fillStyle = i % 2 ? "rgba(255,255,255,.025)" : "transparent"; x.fillRect(0, i * rh, w, rh)
    if (i === 4) { x.fillStyle = "#2b2722"; x.fillRect(0, i * rh, w, 1) }
  })
  for (const l of mx.lanes) {
    const ys = l.deck ? (l.stems?.length ? l.stems : ["vocals", "drums", "bass", "other"]).map((s: string) => ROWS.indexOf(`${l.deck} ${s}`)) : [8]
    const on = S.t >= l.start && S.t < l.end
    x.fillStyle = MOVE_COL[l.move] || "#fff"; x.globalAlpha = on ? 1 : .55
    for (const i of ys) if (i >= 0) {
      const x0 = Math.round(l.start / d * w) + 1, ww = Math.max(2, Math.round((l.end - l.start) / d * w) - 2)
      x.fillRect(x0, i * rh + 3, ww, rh - 6)
      if (!on) { x.fillStyle = "#0a0908"; for (let k = x0 + (i % 2); k < x0 + ww; k += 2) x.fillRect(k, i * rh + 3 + ((k >> 1) % 2), 1, rh - 6); x.fillStyle = MOVE_COL[l.move] || "#fff" }
    }
  }
  x.globalAlpha = 1
  ROWS.forEach((r, i) => { x.fillStyle = "#8d857a"; x.fillText(r.toUpperCase(), 6, i * rh + rh * .68) })
  x.fillStyle = "#fff"; x.fillRect(Math.floor(ph * w), 0, 2, h)
}
addEventListener("resize", () => paint())

onMounted(async () => {
  await loadLib()
  try { const res = await api("/api/latest"); if (res) { showMix(res); log("loaded last mix: " + res.mix.name, "success") } } catch { }
  const live = await api("/api/active").catch(() => null)
  if (live) {
    log(`re-attached to the ${live.kind} job in progress`)
    const r = await watchJob(live, "mixing")
    if (r) { showMix(r); S.say = r.story }
  }
})
</script>

<template>
  <DitherGridScan class="fixed inset-0 -z-10 pointer-events-none" :opacity="0.18" :frame-rate="8" :colors="['#ffb000', '#ff5a1f']" />
  <div class="min-h-screen flex flex-col gap-3 p-3" :class="{ busy: S.busy }">
    <!-- header -->
    <header class="flex items-center gap-4">
      <svg class="moth" width="44" height="44" viewBox="0 0 16 16" shape-rendering="crispEdges" v-html="mothSvg" />
      <div class="font-mono font-extrabold text-2xl tracking-[.32em]">MOTH<small class="block text-[10px] tracking-[.18em] text-muted-foreground font-normal">AN AI DJ THAT ACTUALLY LISTENS</small></div>
      <div class="ml-auto flex items-center gap-3 font-mono text-xs text-muted-foreground">
        <DitherSpinner v-if="S.busy" :size="16" color="orange" />
        <span class="lamp" :class="{ on: S.busy }" />
        <span class="truncate max-w-[40vw]">{{ S.status }}</span>
      </div>
    </header>

    <!-- the deck: A | mixer | B -->
    <div class="grid grid-cols-[1fr_260px_1fr] gap-3">
      <Deck side="A" :track="S.A" :proc="inMix('A') ? m.decks.A : null" :master-bpm="inMix('A') ? m.routine.master_bpm : null"
        :live="liveStems('A')" :spinning="S.playing && deckLive('A')" />

      <section class="border bg-card/90 p-3 flex flex-col gap-3 font-mono">
        <div class="text-[10px] tracking-[.22em] text-muted-foreground flex justify-between"><span>MIXER</span><span>{{ m?.routine?.master_bpm ? m.routine.master_bpm + " BPM" : "" }}</span></div>
        <div class="grid grid-cols-4 gap-1 justify-items-center">
          <div v-for="[k, l, lo, hi] in KNOBS" :key="k" class="flex flex-col items-center gap-1" :title="`${k} = ${knob(k).toFixed(2)} (set by MOTH's learning loop)`">
            <DitherKnob :model-value="knob(k)" :min="lo" :max="hi" :step="0.01" :size="44" class="pointer-events-none" />
            <span class="text-[9px] text-muted-foreground">{{ l }}</span>
          </div>
        </div>
        <div class="flex flex-col gap-2 text-[10px] text-muted-foreground">
          <div>CH A <DitherMeter :value="deckLive('A') ? S.level : 0" class="mt-1" /></div>
          <div>CH B <DitherMeter :value="deckLive('B') ? S.level : 0" class="mt-1" /></div>
          <div>MASTER <DitherMeter :value="S.level" :low="0.6" :high="0.9" class="mt-1" /></div>
        </div>
        <div class="mt-auto">
          <div class="flex justify-between text-[10px] text-muted-foreground"><span>A</span><span>X-FADER · AUTO</span><span>B</span></div>
          <DitherSlider :model-value="S.xf" :min="0" :max="100" color="orange" disabled label="crossfader" />
        </div>
      </section>

      <Deck side="B" :track="S.B" :proc="inMix('B') ? m.decks.B : null" :master-bpm="inMix('B') ? m.routine.master_bpm : null"
        :live="liveStems('B')" :spinning="S.playing && deckLive('B')" />
    </div>

    <!-- performance strip -->
    <section class="border bg-card/90 p-3 flex flex-col gap-2">
      <div class="flex items-center gap-3 font-mono text-xs">
        <DitherButton color="orange" :disabled="!m" class="w-28" @click="togglePlay">{{ S.playing ? "❚❚ PAUSE" : "▶ PLAY" }}</DitherButton>
        <span class="text-muted-foreground tabular-nums">{{ m ? `${fmt(S.t)} / ${fmt(m.duration)}` : "no mix yet" }}</span>
        <span class="truncate">
          <template v-for="l in liveLanes" :key="l.start + l.move + l.deck"><b>{{ l.move }}</b> {{ l.deck }} {{ (l.stems || []).join("+") }} · </template>
        </span>
        <span class="ml-auto text-muted-foreground" v-if="S.mix?.rules">rules {{ S.mix.rules.score }}/100 · {{ S.mix.history?.length || 1 }} take(s)</span>
        <DitherButton :color="S.rated > 0 ? 'green' : 'grey'" variant="hatched" :disabled="!m" @click="rate(1)">▲ {{ S.rated > 0 ? "LOVED" : "LOVE" }}</DitherButton>
        <DitherButton :color="S.rated < 0 ? 'red' : 'grey'" variant="hatched" :disabled="!m" @click="rate(-1)">▼ {{ S.rated < 0 ? "NOTED" : "NAH" }}</DitherButton>
      </div>
      <canvas ref="waveC" class="w-full h-16 block cursor-pointer" @click="seekAt" />
      <canvas ref="lanesC" v-show="isRoutine" class="w-full h-32 block cursor-pointer" @click="seekAt" />
      <audio ref="audio" preload="auto" @play="onPlay" @pause="onPause" @ended="onPause" />
    </section>

    <!-- crate | request + critic | booth -->
    <div class="grid grid-cols-[minmax(280px,1fr)_minmax(320px,1.3fr)_minmax(280px,1fr)] gap-3 grid-rows-[420px]">
      <section class="border bg-card/90 flex flex-col min-h-0">
        <h2 class="px-3 py-2 border-b font-mono text-[10px] tracking-[.22em] text-muted-foreground flex justify-between">CRATE <span>{{ S.lib.length }}</span></h2>
        <input v-model="S.q" placeholder="search title, genre, mood…" class="m-2 px-2 py-1.5 bg-background border font-mono text-xs outline-none focus:border-[#ffb000]" />
        <div class="overflow-auto flex-1 min-h-0">
          <div v-for="t in S.lib" :key="t.id || t.file" class="crow">
            <div class="min-w-0">
              <div class="truncate text-[13px] font-semibold" :title="t.title">{{ t.title }}</div>
              <div class="font-mono text-[10px] text-muted-foreground" v-if="!t.pending">{{ t.bpm.toFixed(1) }} BPM · <span class="text-[#ffb000]">{{ t.camelot }}</span> · {{ t.ears ? t.ears.genre.split("/")[0] : "unheard" }}</div>
            </div>
            <div class="flex gap-1">
              <button v-if="t.pending" class="kbtn" @click="analyzeFile(t.file)">ANALYZE</button>
              <template v-else>
                <button class="kbtn" :class="{ a: S.A?.id === t.id }" @click="S.A = t">A</button>
                <button class="kbtn" :class="{ b: S.B?.id === t.id }" @click="S.B = t">B</button>
                <button class="kbtn" title="add to set list" @click="addSet(t)">+</button>
              </template>
            </div>
          </div>
          <div v-if="!S.lib.length" class="p-4 font-mono text-xs text-muted-foreground">no records yet. drop some audio below.</div>
        </div>
        <label class="m-2 p-3 border border-dashed text-center font-mono text-[10px] text-muted-foreground cursor-pointer" :class="{ 'border-[#ffb000] text-[#ffb000]': over }"
          @dragenter.prevent="over = true" @dragover.prevent="over = true" @dragleave="over = false" @drop.prevent="over = false; upload($event.dataTransfer?.files)">
          drop audio here (mp3 / m4a / wav / flac)
          <input type="file" multiple accept="audio/*" hidden @change="upload(($event.target as HTMLInputElement).files)" />
        </label>
      </section>

      <section class="border bg-card/90 flex flex-col gap-3 p-3 min-h-0 overflow-auto [&>*]:shrink-0">
        <textarea v-model="S.brief" rows="3" placeholder='tell MOTH the vibe, e.g. "oil and water: make these two lock, party energy"'
          class="w-full resize-none px-2 py-2 bg-background border font-mono text-xs outline-none focus:border-[#ffb000]" />
        <DitherButton color="orange" :disabled="!canPerform" :loading="S.busy" class="w-full" @click="startMix([S.A.id, S.B.id], false)">
          PERFORM {{ S.A ? "A" : "–" }} × {{ S.B ? "B" : "–" }}
        </DitherButton>
        <div class="font-mono text-[10px] text-muted-foreground flex flex-wrap gap-1 items-center">
          <span>set list:</span>
          <span v-for="(t, i) in S.set" :key="t.id" class="chip" title="remove" @click="S.set.splice(i, 1)">{{ t.title.slice(0, 22) }} ×</span>
          <button v-if="S.set.length >= 2" class="underline ml-auto" :disabled="S.busy" title="long crossfade set from everything in the set list" @click="startMix(S.set.map(t => t.id), true)">take over ({{ S.set.length }})</button>
          <span v-else-if="!S.set.length">add tracks with +</span>
        </div>
        <div v-if="critic" class="border p-3 flex flex-col gap-2">
          <div class="flex justify-between items-center font-mono text-[10px] tracking-[.1em] text-muted-foreground">
            <span class="truncate">{{ S.mix.plan?.title || "ROUTINE" }}</span>
            <DitherBadge :color="scoreColor(critic.weighted)" class="font-mono">{{ critic.weighted }}</DitherBadge>
          </div>
          <div class="italic text-sm text-muted-foreground">“{{ critic.verdict }}”</div>
          <div class="text-xs"><span class="text-muted-foreground">biggest flaw:</span> {{ critic.biggest_flaw }}</div>
          <div class="grid grid-cols-3 gap-x-3 gap-y-1">
            <div v-for="k in ['performance', 'beat_sync', 'phrase_fit', 'low_end', 'vocals', 'human_feel']" :key="k" class="font-mono text-[9px] text-muted-foreground">
              {{ k.replace("_", " ") }}<i class="axis"><s :style="{ width: (critic.scores[k] || 0) * 10 + '%' }" /></i>
            </div>
          </div>
        </div>
        <div v-if="isRoutine" class="flex flex-col">
          <button v-for="l in m.lanes" :key="l.start + l.move + l.deck + (l.stems || []).join()" class="lane-row" :class="{ live: S.t >= l.start && S.t < l.end }" @click="seek(l.start - 1, true)">
            <span class="font-mono text-[10px] text-muted-foreground w-20 shrink-0">{{ fmt(l.start) }} {{ l.move.toUpperCase() }} {{ l.deck || "" }}</span>
            <span class="text-xs text-left">{{ l.note }}</span>
          </button>
        </div>
      </section>

      <section class="border bg-card/90 flex flex-col min-h-0">
        <h2 class="px-3 py-2 border-b font-mono text-[10px] tracking-[.22em] text-muted-foreground">THE BOOTH</h2>
        <div class="p-3 flex gap-3 items-start border-b">
          <svg class="moth shrink-0" width="56" height="56" viewBox="0 0 16 16" shape-rendering="crispEdges" v-html="mothSvg" />
          <div class="bubble text-[13px] leading-snug">{{ S.say }}</div>
        </div>
        <DitherConsole :lines="S.log" title="moth.log" follow :caret="S.busy" class="flex-1 min-h-0 m-2" />
      </section>
    </div>
  </div>
</template>

<style>
.lamp { width: 8px; height: 8px; background: #28d26e; box-shadow: 0 0 10px #28d26e; }
.lamp.on { background: #ffb000; box-shadow: 0 0 12px #ffb000; animation: blink .6s steps(2) infinite; }
@keyframes blink { 50% { opacity: .2; } }
.moth { filter: drop-shadow(0 0 8px rgba(255, 176, 0, .35)); }
.moth .wing { transform-box: fill-box; }
.moth .wl { transform-origin: right center; }
.moth .wr { transform-origin: left center; }
.busy .moth .wl, .busy .moth .wr { animation: flap .22s steps(2) infinite; }
@keyframes flap { 50% { transform: scaleX(.55); } }
canvas { image-rendering: pixelated; }
.crow { display: flex; align-items: center; gap: 8px; padding: 8px 12px; border-bottom: 1px solid var(--border); }
.crow:hover { background: rgba(255, 176, 0, .04); }
.kbtn { font: 700 10px var(--font-mono); padding: 4px 7px; border: 1px solid var(--border); color: var(--foreground); background: #0d0c0a; }
.kbtn:hover { border-color: #ffb000; color: #ffb000; }
.kbtn.a { background: #ffa01e; color: #0a0908; border-color: #ffa01e; }
.kbtn.b { background: #4696ff; color: #0a0908; border-color: #4696ff; }
.chip { border: 1px solid var(--border); padding: 1px 5px; cursor: pointer; color: var(--foreground); }
.axis { display: block; height: 4px; background: var(--border); margin-top: 2px; }
.axis s { display: block; height: 100%; background: #ffb000; }
.lane-row { display: flex; gap: 8px; padding: 6px 4px; border-bottom: 1px solid var(--border); text-align: left; }
.lane-row:hover { background: rgba(255, 176, 0, .05); }
.lane-row.live { background: rgba(255, 176, 0, .1); box-shadow: inset 2px 0 #ffb000; }
.bubble { background: #15120e; border: 1px solid var(--border); padding: 8px 10px; flex: 1; }
</style>
