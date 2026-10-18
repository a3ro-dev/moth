import { fileURLToPath } from "node:url"
import vue from "@vitejs/plugin-vue"
import tailwindcss from "@tailwindcss/vite"
import { defineConfig } from "vite"

const api = { target: "http://127.0.0.1:8077" }
export default defineConfig({
  plugins: [vue(), tailwindcss()],
  resolve: { alias: { "@dither-kit": fileURLToPath(new URL("./src/dither-kit", import.meta.url)) } },
  server: { port: 5177, proxy: { "/api": api, "/audio": api } },
})
