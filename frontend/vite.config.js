import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// === ProjectGuard Mini Vite Config (v6.6) ===
export default defineConfig({
  plugins: [react()],
  server: {
    host: '0.0.0.0',   // чтобы открыть с телефона по IP
    port: 5173,        // твой порт разработки
  },
  build: {
    outDir: 'dist',    // продакшн-сборка сюда
    rollupOptions: {
      output: {
        entryFileNames: `assets/[name]-[hash].js`,
        chunkFileNames: `assets/[name]-[hash].js`,
        assetFileNames: `assets/[name]-[hash][extname]`
      }
    }
  },
  preview: {
    host: '0.0.0.0',
    port: 5173,
  },
})

