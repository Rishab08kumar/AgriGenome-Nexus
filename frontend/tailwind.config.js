/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'agri-green': '#00ff88',
        'agri-dark': '#0a0f0a',
        'agri-gold': '#ffd700',
        'agri-blue': '#00b4ff',
        'agri-glow': '#39ff14',
      },
      fontFamily: {
        rajdhani: ['Rajdhani', 'sans-serif'],
        space: ['Space Grotesk', 'sans-serif'],
      },
      animation: {
        'float': 'float 6s ease-in-out infinite',
        'pulse-glow': 'pulse-glow 2s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'shimmer': 'shimmer 2s linear infinite',
        'scan-line': 'scan-line 3s linear infinite',
      },
      keyframes: {
        float: {
          '0%, 100%': { transform: 'translateY(0)' },
          '50%': { transform: 'translateY(-10px)' },
        },
        'pulse-glow': {
          '0%, 100%': { opacity: 1, boxShadow: '0 0 15px rgba(0,255,136,0.5)' },
          '50%': { opacity: .5, boxShadow: '0 0 30px rgba(0,255,136,0.8)' },
        },
        shimmer: {
          'from': { backgroundPosition: '200% 0' },
          'to': { backgroundPosition: '-200% 0' },
        },
        'scan-line': {
          '0%': { top: '0%' },
          '100%': { top: '100%' },
        }
      }
    },
  },
  plugins: [],
}
