import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  base: process.env.GITHUB_PAGES === 'true' ? '/AI-Operating-System-for-Ideas/' : '/',
  server: {
    port: 5173,
    host: '127.0.0.1'
  }
})

