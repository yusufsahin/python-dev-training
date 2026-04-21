import path from 'path'
import tailwindcss from '@tailwindcss/vite'
import react from '@vitejs/plugin-react'
import { defineConfig } from 'vite'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react(), tailwindcss()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
  build: {
    chunkSizeWarningLimit: 550,
    rollupOptions: {
      output: {
        manualChunks(id) {
          if (!id.includes('node_modules')) return
          if (id.includes('react-dom')) return 'vendor-react-dom'
          if (id.includes('/react/')) return 'vendor-react'
          if (id.includes('@reduxjs/toolkit') || id.includes('react-redux')) return 'vendor-redux'
          if (id.includes('radix-ui')) return 'vendor-radix'
          if (id.includes('lucide-react')) return 'vendor-lucide'
          if (
            id.includes('react-hook-form') ||
            id.includes('@hookform/resolvers') ||
            id.includes('/zod/')
          ) {
            return 'vendor-form'
          }
        },
      },
    },
  },
})
