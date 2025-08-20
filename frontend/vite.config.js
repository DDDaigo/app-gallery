import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import tailwindcss from '@tailwindcss/vite'

// 環境変数でホストやHMR先を切り替え（Dockerfileは触らない）
const allowed = (process.env.VITE_ALLOWED_HOSTS || 'gallery.localhost')
  .split(',')
  .map(s => s.trim())
  .filter(Boolean)

const hmrHost = process.env.VITE_HMR_HOST || allowed[0]
const hmrPort = Number(process.env.VITE_HMR_PORT || 443) // 本番は 443
const hmrProtocol = process.env.VITE_HMR_PROTOCOL || (hmrPort === 443 ? 'wss' : 'ws')

export default defineConfig({
  plugins: [vue(), tailwindcss()],
  server: {
    host: true,          // 0.0.0.0 で待受（--host と同等）
    port: 5173,
    strictPort: true,    // 5173 が埋まってても勝手に 5174 に逃げない（Traefik 5173固定のため重要）
    allowedHosts: allowed,                 // ★ 本番ドメインを許可
    hmr: { host: hmrHost, port: hmrPort, protocol: hmrProtocol }, // ★ HMR を本番ドメイン/443に合わせる
  },
})


// // dev用
// import { defineConfig } from 'vite'
// import vue from '@vitejs/plugin-vue'
// import tailwindcss from '@tailwindcss/vite'


// // https://vite.dev/config/
// export default defineConfig({
//   plugins: [
//     vue(),
//     tailwindcss(),
//   ],
// })




