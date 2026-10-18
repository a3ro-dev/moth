// shared canvas helpers: 3-band waveform (low/mid/high) and the Bayer matrix the platter dithers with
export const BAND = ["#ff5a1f", "#ffb000", "#f5f1e6"]
export const BAYER4 = [0, 8, 2, 10, 12, 4, 14, 6, 3, 11, 1, 9, 15, 7, 13, 5].map(v => (v + 0.5) / 16)

export type Region = { a: number; b: number; color: string }

export function drawWave(canvas: HTMLCanvasElement, wave: number[][] | null | undefined,
  opts: { regions?: Region[]; marks?: Region[]; playhead?: number } = {}) {
  const w = canvas.width = canvas.clientWidth, h = canvas.height = canvas.clientHeight, x = canvas.getContext("2d")!
  x.clearRect(0, 0, w, h)
  if (!wave) return
  const n = wave[0].length
  for (const r of opts.regions || []) { x.fillStyle = r.color; x.fillRect(r.a * w, 0, (r.b - r.a) * w, h) }
  // chunky 2px columns quantized to 2px rows: reads as pixels, like the kit
  for (const b of [0, 1, 2]) {
    x.fillStyle = BAND[b]
    for (let i = 0; i < w; i += 3) {
      const v = wave[b][Math.floor(i / w * n)] * [1, .8, .55][b]
      const hh = Math.max(2, Math.round(v * h * .92 / 2) * 2)
      x.fillRect(i, Math.round((h - hh) / 4) * 2, 2, hh)
    }
  }
  for (const m of opts.marks || []) { x.fillStyle = m.color; x.fillRect(m.a * w, 0, 2, h) }
  if (opts.playhead != null) { x.fillStyle = "#fff"; x.fillRect(Math.floor(opts.playhead * w), 0, 2, h) }
}

export const fmt = (s: number) => `${Math.floor(s / 60)}:${String(Math.floor(s % 60)).padStart(2, "0")}`
