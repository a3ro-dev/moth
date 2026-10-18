<script setup lang="ts">
import { computed, nextTick, onMounted, reactive, ref, watch } from "vue"
import { DitherButton, DitherSlider, DitherSpinner } from "@dither-kit"
import Deck from "./Deck.vue"
import { drawWave, fmt } from "./wave"

const S = reactive({ lib: [] as any[], A: null as any, B: null as any, mix: null as any, pending: null as any,
  busy: false, status: "pick two records, say the vibe, hit perform", q: "", brief: "", t: 0, playing: false, xf: 50, rated: 0 })
const api = async (path: string, opts?: RequestInit) => { const r = await fetch(path, opts); if (!r.ok) throw new Error((await r.text()) || String(r.status)); return r.json() }

// ---------- crate
async function loadLib() { S.lib = await api("/api/library?q=" + encodeURIComponent(S.q)) }
let qt = 0
watch(() => S.q, () => { clearTimeout(qt); qt = window.setTimeout(loadLib, 200) })
const over = ref(false)
async function upload(files: FileList | null | undefined) {
  if (!files?.length) return
  const fd = new FormData(); [...files].forEach(f => fd.append("files", f))
  watchJob(await api("/api/upload", { method: "POST", body: fd }), "reading the new records")
}
async function analyzeFile(f: string) { watchJob(await api("/api/analyze/" + encodeURIComponent(f), { method: "POST" }), "listening to it") }

// ---------- jobs: every rendered take lands on the decks as soon as it exists
function offer(r: any) {
  if (S.mix?.mix.file === r.mix.file) return
  if (S.playing) { S.pending = r; return }  // never yank the record mid-listen
  showMix(r)
}
async function watchJob(job: any, label: string) {
  S.busy = true; S.status = label; let seen = 0
  while (true) {
    await new Promise(r => setTimeout(r, 2000))
    const j = await api("/api/jobs/" + job.id)
    if (j.status === "queued") S.status = "waiting for the other job to finish"
    for (const ev of j.events.slice(seen)) if (ev.msg) S.status = ev.msg
    seen = j.events.length
    if (j.preview) offer(j.preview)
    if (j.status === "done") { S.busy = false; loadLib(); if (j.result?.mix) offer(j.result); S.status = j.result?.mix ? "done. that's my best take" : "done"; return }
    if (j.status === "error") { S.busy = false; S.status = "went sideways: " + j.error; return }
  }
}
async function perform() {
  if (S.busy || !canPerform.value) return
  S.busy = true; S.status = "on it"
  await watchJob(await api("/api/mix", { method: "POST", headers: { "content-type": "application/json" },
    body: JSON.stringify({ ids: [S.A.id, S.B.id], brief: S.brief.trim() }) }), "on it")
}
const canPerform = computed(() => S.A && S.B && S.A.id !== S.B.id)

// ---------- the loaded mix
const audio = ref<HTMLAudioElement | null>(null)
const m = computed(() => S.mix?.mix)
const byId = (id: string) => S.lib.find(t => t.id === id)
function showMix(r: any) {
  S.mix = r; S.pending = null; S.rated = 0; S.t = 0
  for (const [k, d] of Object.entries<any>(r.mix.decks || {})) { const t = byId(d.id); if (t) (S as any)[k] = t }
  audio.value!.src = "/audio/mix/" + encodeURIComponent(r.mix.file)
  nextTick(paint)
}
const inMix = (side: string) => !!m.value?.decks && m.value.decks[side]?.id === (S as any)[side]?.id
const liveStems = (side: string) => !inMix(side) ? [] : (m.value?.lanes || [])
  .filter((l: any) => l.deck === side && S.t >= l.start && S.t < l.end)
  .flatMap((l: any) => l.stems?.length ? l.stems : ["vocals", "drums", "bass", "other"])
const critic = computed(() => S.mix?.critiques?.[0])

// ---------- transport
function togglePlay() { audio.value!.paused ? audio.value!.play() : audio.value!.pause() }
function tick() {
  if (!audio.value) return
  S.t = audio.value.currentTime
  const a = liveStems("A").length > 0, b = liveStems("B").length > 0
  S.xf += ((a && !b ? 0 : b && !a ? 100 : 50) - S.xf) * .15
  paint()
  if (S.playing) requestAnimationFrame(tick)
}
function onPlay() { S.playing = true; requestAnimationFrame(tick) }
function onPause() { S.playing = false; if (S.pending) showMix(S.pending) }
function seekAt(e: MouseEvent) {
  if (!m.value) return
  audio.value!.currentTime = e.offsetX / (e.currentTarget as HTMLElement).clientWidth * m.value.duration
  S.t = audio.value!.currentTime; paint()
}
async function rate(v: number) {
  if (!S.mix) return
  const note = prompt(v > 0 ? "what worked? (optional)" : "what's off? MOTH reads this next time") ?? ""
  await fetch("/api/rate", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ name: m.value.file, rating: v, note }) })
  S.rated = v
}

// ---------- waveform + one vocal row and one beat row per deck
const waveC = ref<HTMLCanvasElement | null>(null), lanesC = ref<HTMLCanvasElement | null>(null)
const ROWS: [string, string, string][] = [["A", "vox", "#ffb000"], ["A", "beat", "#a8640f"], ["B", "vox", "#6aa8ff"], ["B", "beat", "#2f5f9e"]]
function paint() {
  if (!waveC.value || !lanesC.value) return
  const mx = m.value, ph = mx ? S.t / mx.duration : undefined
  drawWave(waveC.value, mx?.waveform, { playhead: ph })
  const cv = lanesC.value, w = cv.width = cv.clientWidth, h = cv.height = cv.clientHeight, x = cv.getContext("2d")!
  x.clearRect(0, 0, w, h)
  if (!mx?.lanes) return
  const rh = h / ROWS.length
  ROWS.forEach(([deck, kind, col], i) => {
    x.fillStyle = col
    for (const l of mx.lanes) {
      if (l.deck !== deck) continue
      const stems = l.stems?.length ? l.stems : ["vocals", "drums"]
      if (!stems.some((s: string) => (s === "vocals") === (kind === "vox"))) continue
      x.globalAlpha = S.t >= l.start && S.t < l.end ? 1 : .45
      x.fillRect(Math.round(l.start / mx.duration * w), i * rh + 2, Math.max(2, Math.round((l.end - l.start) / mx.duration * w) - 1), rh - 4)
    }
  })
  x.globalAlpha = 1; x.fillStyle = "#fff"; x.fillRect(Math.floor(ph! * w), 0, 2, h)
}
addEventListener("resize", () => paint())

onMounted(async () => {
  await loadLib()
  try { const r = await api("/api/latest"); if (r) showMix(r) } catch { }
  const live = await api("/api/active").catch(() => null)
  if (live) watchJob(live, "picking up where i left off")
})
</script>

<template>
  <div class="h-screen flex flex-col gap-5 px-8 py-6 max-w-[1500px] mx-auto">
    <header class="flex items-baseline gap-6">
      <div class="font-mono font-extrabold text-xl tracking-[.4em]">MOTH</div>
      <div class="flex items-center gap-2 font-mono text-xs text-muted-foreground min-w-0">
        <DitherSpinner v-if="S.busy" :size="12" color="orange" />
        <span class="truncate">{{ S.status }}</span>
      </div>
    </header>

    <!-- the deck -->
    <div class="grid grid-cols-[1fr_220px_1fr] items-center gap-8">
      <Deck side="A" :track="S.A" :bpm="inMix('A') ? m.routine.master_bpm : null" :live="liveStems('A')" :spinning="S.playing && liveStems('A').length > 0" />
      <div class="flex flex-col items-center gap-3 font-mono">
        <DitherButton color="orange" :disabled="!m" class="w-full" @click="togglePlay">{{ S.playing ? "❚❚ PAUSE" : "▶ PLAY" }}</DitherButton>
        <div class="text-xs text-muted-foreground tabular-nums">{{ m ? `${fmt(S.t)} / ${fmt(m.duration)}` : "--:--" }}</div>
        <DitherSlider :model-value="S.xf" :min="0" :max="100" color="orange" disabled label="crossfader" class="w-full" />
        <div class="flex gap-2 w-full">
          <button class="rate" :class="{ up: S.rated > 0 }" :disabled="!m" @click="rate(1)">▲ love</button>
          <button class="rate" :class="{ down: S.rated < 0 }" :disabled="!m" @click="rate(-1)">▼ nah</button>
        </div>
      </div>
      <Deck side="B" :track="S.B" :bpm="inMix('B') ? m.routine.master_bpm : null" :live="liveStems('B')" :spinning="S.playing && liveStems('B').length > 0" />
    </div>

    <!-- the mix -->
    <div class="flex flex-col gap-1 cursor-pointer" @click="seekAt">
      <canvas ref="waveC" class="w-full h-20 block pointer-events-none" />
      <canvas ref="lanesC" class="w-full h-10 block pointer-events-none" />
      <div class="flex justify-between font-mono text-[10px] text-muted-foreground pointer-events-none">
        <span>{{ S.mix?.plan?.title || "" }}</span>
        <span v-if="S.pending" class="text-[#ffb000]">a better take is ready, it loads when you pause</span>
        <span v-else-if="critic">critic {{ critic.weighted }}/10 · {{ critic.verdict }}</span>
      </div>
    </div>

    <!-- pick + ask -->
    <div class="grid grid-cols-[1fr_380px] gap-8 flex-1 min-h-0">
      <div class="flex flex-col min-h-0 border-t pt-3"
        @dragenter.prevent="over = true" @dragover.prevent="over = true" @dragleave="over = false" @drop.prevent="over = false; upload($event.dataTransfer?.files)"
        :class="{ 'outline outline-1 outline-[#ffb000]': over }">
        <div class="flex items-center gap-3 mb-2">
          <input v-model="S.q" placeholder="search records" class="flex-1 bg-transparent font-mono text-sm outline-none placeholder:text-muted-foreground" />
          <label class="font-mono text-[10px] text-muted-foreground cursor-pointer hover:text-foreground">+ add audio
            <input type="file" multiple accept="audio/*" hidden @change="upload(($event.target as HTMLInputElement).files)" /></label>
        </div>
        <div class="overflow-auto flex-1 min-h-0">
          <div v-for="t in S.lib" :key="t.id || t.file" class="crow">
            <div class="min-w-0 flex-1 truncate text-sm" :title="t.title">{{ t.title }}</div>
            <span class="font-mono text-[11px] text-muted-foreground w-28 text-right" v-if="!t.pending">{{ t.bpm.toFixed(0) }} BPM · {{ t.camelot }}</span>
            <button v-if="t.pending" class="load wide" @click="analyzeFile(t.file)">analyze</button>
            <template v-else>
              <button class="load" :class="{ a: S.A?.id === t.id }" @click="S.A = t">A</button>
              <button class="load" :class="{ b: S.B?.id === t.id }" @click="S.B = t">B</button>
            </template>
          </div>
          <div v-if="!S.lib.length" class="py-4 font-mono text-xs text-muted-foreground">no records yet. drop audio files here.</div>
        </div>
      </div>

      <div class="flex flex-col gap-3 border-t pt-3">
        <textarea v-model="S.brief" rows="3" placeholder="the vibe, e.g. make these two lock, party energy"
          class="w-full resize-none bg-transparent font-mono text-sm outline-none placeholder:text-muted-foreground" />
        <DitherButton color="orange" :disabled="!canPerform || S.busy" class="w-full" @click="perform">
          {{ S.busy ? "MIXING…" : canPerform ? `PERFORM ${S.A.title.split(" (")[0]} × ${S.B.title.split(" (")[0]}` : "LOAD A AND B" }}
        </DitherButton>
        <div class="font-mono text-[10px] text-muted-foreground">first take plays in ~7 min, MOTH keeps revising after that</div>
      </div>
    </div>
    <audio ref="audio" preload="auto" @play="onPlay" @pause="onPause" @ended="onPause" />
  </div>
</template>

<style>
canvas { image-rendering: pixelated; }
.crow { display: flex; align-items: center; gap: 10px; padding: 7px 0; border-bottom: 1px solid #1c1915; }
.load { font: 700 10px var(--font-mono); width: 26px; padding: 3px 0; border: 1px solid var(--border); color: var(--muted-foreground); }
.load:hover { color: var(--foreground); border-color: var(--foreground); }
.load.a { background: #ffa01e; color: #0a0908; border-color: #ffa01e; }
.load.b { background: #4696ff; color: #0a0908; border-color: #4696ff; }
.load.wide { width: auto; padding: 3px 8px; }
.rate { flex: 1; font: 700 10px var(--font-mono); letter-spacing: .1em; padding: 5px 0; border: 1px solid var(--border); color: var(--muted-foreground); }
.rate:hover:not(:disabled) { color: var(--foreground); }
.rate:disabled { opacity: .3; }
.rate.up { color: #28d26e; border-color: #28d26e; }
.rate.down { color: #ff4d4d; border-color: #ff4d4d; }
</style>
