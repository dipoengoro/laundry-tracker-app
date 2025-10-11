import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  server: {
    host: true, // penting untuk Docker agar bisa diakses dari host
    port: 5173
  }
})