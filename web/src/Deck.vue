<script setup lang="ts">
import { computed, onBeforeUnmount, onMounted, ref, watch } from "vue"
import { BAYER4 } from "./wave"

const props = defineProps<{
  side: "A" | "B"
  track: any | null
  bpm: number | null      // the BPM it plays at in the loaded mix (null = native)
  live: string[]          // stems of this deck sounding at the playhead
  spinning: boolean
}>()

const rgb = computed(() => props.side === "A" ? [255, 160, 30] : [70, 150, 255])
const STEMS = [["vocals", "VOX"], ["drums", "DRUMS"], ["bass", "BASS"], ["other", "MELODY"]]

// platter: a dithered record with a cue mark that turns while the deck plays
const plat = ref<HTMLCanvasElement | null>(null)
let angle = 0, raf = 0, last = 0
function paint() {
  const c = plat.value
  if (!c) return
  const S = Math.floor(c.clientWidth / 3)
  c.width = c.height = S
  const x = c.getContext("2d")!, img = x.createImageData(S, S), d = img.data, r0 = S / 2
  const [cr, cg, cb] = rgb.value, on = !!props.track
  for (let py = 0; py < S; py++) for (let px = 0; px < S; px++) {
    const dx = px - r0 + .5, dy = py - r0 + .5, r = Math.hypot(dx, dy) / r0
    if (r > 1) continue
    const a = Math.atan2(dy, dx)
    let v: number, col = [236, 231, 220]
    if (r < .3) { v = on ? .8 : .1; col = on ? [cr, cg, cb] : col; if (r < .05) v = 0 }
    else v = .05 + (Math.sin(r * 90) + 1) / 2 * .08 + Math.max(0, Math.cos(2 * (a - .8))) ** 6 * .3
    if (on && r > .36 && r < .94 && Math.abs(((a - angle + Math.PI * 3) % (Math.PI * 2)) - Math.PI) < .05) { v = 1; col = [cr, cg, cb] }
    const lit = v > BAYER4[(py % 4) * 4 + (px % 4)], i = (py * S + px) * 4
    d[i] = lit ? col[0] : 17; d[i + 1] = lit ? col[1] : 15; d[i + 2] = lit ? col[2] : 13; d[i + 3] = 255
  }
  x.putImageData(img, 0, 0)
}
function loop(ts: number) {
  angle += (last ? (ts - last) / 1000 : 0) * Math.PI * 2 * 33.3 / 60; last = ts
  paint()
  if (props.spinning) raf = requestAnimationFrame(loop); else { raf = 0; last = 0 }
}
watch(() => props.spinning, s => { if (s && !raf) raf = requestAnimationFrame(loop) })
watch(() => props.track, paint)
onMounted(() => { paint(); addEventListener("resize", paint) })
onBeforeUnmount(() => { cancelAnimationFrame(raf); removeEventListener("resize", paint) })
</script>

<template>
  <section class="flex items-center gap-5 min-w-0" :class="side === 'B' ? 'flex-row-reverse text-right' : ''">
    <canvas ref="plat" class="platter" />
    <div class="min-w-0 flex-1 flex flex-col gap-2">
      <div class="font-mono text-xs tracking-[.3em]" :style="{ color: `rgb(${rgb})` }">DECK {{ side }}</div>
      <div class="truncate text-lg font-semibold" :title="track?.title">{{ track?.title || "empty" }}</div>
      <div class="font-mono text-sm text-muted-foreground" v-if="track">
        {{ (bpm ?? track.bpm).toFixed(0) }} BPM · {{ track.key }}
      </div>
      <div class="flex gap-1.5 mt-1" :class="side === 'B' ? 'justify-end' : ''">
        <span v-for="[k, l] in STEMS" :key="k" class="pad font-mono" :class="{ on: live.includes(k) }" :style="{ '--c': `rgb(${rgb})` }">{{ l }}</span>
      </div>
    </div>
  </section>
</template>

<style scoped>
.platter { width: 132px; height: 132px; image-rendering: pixelated; border-radius: 50%; flex: none; box-shadow: 0 0 0 5px #181512; }
.pad { font-size: 10px; font-weight: 700; letter-spacing: .1em; padding: 5px 8px; border: 1px solid var(--border); color: var(--muted-foreground); }
.pad.on { color: #0a0908; background: var(--c); border-color: var(--c); }
</style>
