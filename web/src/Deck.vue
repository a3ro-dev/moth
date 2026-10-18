<script setup lang="ts">
import { computed, onBeforeUnmount, onMounted, ref, watch } from "vue"
import { DitherBadge, DitherSlider } from "@dither-kit"
import { BAYER4, drawWave, fmt } from "./wave"

const props = defineProps<{
  side: "A" | "B"
  track: any | null          // library card
  proc: { stretch_pct: number; semitones: number } | null  // what the routine did to this deck
  masterBpm: number | null
  live: string[]             // stems of this deck sounding at the playhead
  spinning: boolean
}>()

const color = computed(() => props.side === "A" ? "orange" : "blue")
const rgb = computed(() => props.side === "A" ? [255, 160, 30] : [70, 150, 255])
const STEMS = [["vocals", "VOX"], ["drums", "DRM"], ["bass", "BAS"], ["other", "INST"]]
const tempo = computed(() => props.proc?.stretch_pct ?? 0)
const bpm = computed(() => props.track ? (props.masterBpm ?? props.track.bpm) : null)

// ---- platter: a dithered record, grooves + label, a cue mark that rotates while the deck plays
const plat = ref<HTMLCanvasElement | null>(null)
const wave = ref<HTMLCanvasElement | null>(null)
let angle = 0, raf = 0, last = 0
function paintPlatter() {
  const c = plat.value
  if (!c) return
  const CELL = 3, S = Math.floor(c.clientWidth / CELL)
  c.width = c.height = S
  const x = c.getContext("2d")!, img = x.createImageData(S, S), d = img.data, r0 = S / 2
  const [cr, cg, cb] = rgb.value, on = !!props.track
  for (let py = 0; py < S; py++) for (let px = 0; px < S; px++) {
    const dx = px - r0 + .5, dy = py - r0 + .5, r = Math.hypot(dx, dy) / r0
    if (r > 1) continue
    const a = Math.atan2(dy, dx)
    let v: number, col = [236, 231, 220]
    if (r < .34) {                                          // label
      v = on ? (r > .3 ? .35 : .75 + .2 * Math.cos(a - angle)) : .12; col = on ? [cr, cg, cb] : col
      if (r < .05) v = 0                                    // spindle
    } else {
      const groove = (Math.sin(r * 90) + 1) / 2 * .1        // vinyl grooves
      const sheen = Math.max(0, Math.cos(2 * (a - angle * .15 - .8))) ** 6 * .35  // light catches the record
      v = .06 + groove + sheen
      if (r > .96) v = .32                                  // rim
    }
    const cue = Math.abs(((a - angle + Math.PI * 3) % (Math.PI * 2)) - Math.PI) < .05 && r > .4 && r < .94
    if (cue && on) { v = 1; col = [cr, cg, cb] }
    const lit = v > BAYER4[(py % 4) * 4 + (px % 4)]
    const i = (py * S + px) * 4
    d[i] = lit ? col[0] : 18; d[i + 1] = lit ? col[1] : 16; d[i + 2] = lit ? col[2] : 14; d[i + 3] = 255
  }
  x.putImageData(img, 0, 0)
}
function loop(ts: number) {
  const dt = last ? (ts - last) / 1000 : 0; last = ts
  if (props.spinning) angle += dt * Math.PI * 2 * (33.3 / 60) * (1 + tempo.value / 100)
  paintPlatter()
  raf = props.spinning ? requestAnimationFrame(loop) : 0
  if (!raf) last = 0
}
watch(() => props.spinning, s => { if (s && !raf) raf = requestAnimationFrame(loop) })
watch(() => [props.track, props.side], () => { paintPlatter(); paintWave() })

function paintWave() {
  if (!wave.value) return
  const t = props.track
  drawWave(wave.value, t?.waveform, {
    regions: (t?.sections || []).filter((s: any) => s.vocals).map((s: any) =>
      ({ a: s.start_s / t.duration, b: s.end_s / t.duration, color: "rgba(198,255,61,.08)" })),
  })
}
const onResize = () => { paintPlatter(); paintWave() }
onMounted(() => { onResize(); addEventListener("resize", onResize) })
onBeforeUnmount(() => { cancelAnimationFrame(raf); removeEventListener("resize", onResize) })
</script>

<template>
  <section class="deck border bg-card/90 p-3 flex flex-col gap-3 min-w-0" :class="{ dim: !track }">
    <header class="flex items-start gap-3">
      <div class="font-mono font-extrabold text-4xl leading-none" :style="{ color: track ? `rgb(${rgb})` : 'var(--border)' }">{{ side }}</div>
      <div class="min-w-0 flex-1">
        <div class="truncate font-semibold text-[15px]" :title="track?.title">{{ track?.title || "no record loaded" }}</div>
        <div class="truncate text-xs italic text-muted-foreground">{{ track?.ears?.vibe || (track ? "not heard yet" : "pick one from the crate") }}</div>
      </div>
      <DitherBadge v-if="track" :color="color" class="font-mono text-xs">{{ track.camelot }}</DitherBadge>
    </header>

    <div class="flex gap-3 items-center">
      <canvas ref="plat" class="platter" :class="{ 'order-2': side === 'B' }" />
      <div class="flex-1 flex flex-col gap-2 min-w-0 font-mono">
        <div class="lcd">
          <div class="flex justify-between text-[10px] text-muted-foreground"><span>BPM</span><span>KEY</span></div>
          <div class="flex justify-between items-baseline">
            <b class="text-3xl tabular-nums">{{ bpm ? bpm.toFixed(1) : "---.-" }}</b>
            <b class="text-xl" :style="{ color: `rgb(${rgb})` }">{{ track?.key || "--" }}</b>
          </div>
          <div class="flex justify-between text-[10px] text-muted-foreground">
            <span>{{ track ? `orig ${track.bpm.toFixed(1)}` : "" }}</span>
            <span>{{ proc?.semitones ? `${proc.semitones > 0 ? "+" : ""}${proc.semitones} st` : (track ? fmt(track.duration) : "") }}</span>
          </div>
        </div>
        <div>
          <div class="flex justify-between text-[10px] text-muted-foreground"><span>TEMPO</span><span>{{ tempo > 0 ? "+" : "" }}{{ tempo.toFixed(1) }}%</span></div>
          <DitherSlider :model-value="tempo" :min="-18" :max="18" :step="0.1" :color="color" ticks disabled label="tempo" />
        </div>
      </div>
    </div>

    <div class="grid grid-cols-4 gap-2">
      <div v-for="[k, l] in STEMS" :key="k" class="pad font-mono" :class="{ on: live.includes(k) }"
        :style="{ '--c': `rgb(${rgb})` }">{{ l }}</div>
    </div>
    <canvas ref="wave" class="w-full h-12 block" />
  </section>
</template>

<style scoped>
.deck.dim { opacity: .75; }
.platter { width: 150px; height: 150px; image-rendering: pixelated; border-radius: 50%; flex: none;
  box-shadow: 0 0 0 6px #1a1714, 0 0 0 7px var(--border); }
.lcd { background: #0d0c0a; border: 1px solid var(--border); padding: 6px 8px; }
.pad { text-align: center; font-size: 11px; font-weight: 700; letter-spacing: .12em; padding: 9px 0; border: 1px solid var(--border);
  color: var(--muted-foreground); background: #0d0c0a; transition: background .08s, color .08s; }
.pad.on { color: #0a0908; background: var(--c); border-color: var(--c); box-shadow: 0 0 14px var(--c); }
</style>
