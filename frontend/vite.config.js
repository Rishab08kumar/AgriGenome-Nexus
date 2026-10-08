
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],

  server: {
    allowedHosts: true,

    proxy: {
      // Existing AgriGenome-Nexus API endpoints
      '/api': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
      },

      // NEW: Geo-Adaptive Crop Suitability
      '/geo-crop-suitability': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
      },
    },
  },
})
