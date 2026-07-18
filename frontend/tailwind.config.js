/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        background: '#020408',
        foreground: '#F8FAFC',
        accentPrimary: '#6366F1', // Indigo Aether
        accentCyan: '#06B6D4',    // Cyan Spark
        slateGlass: 'rgba(15, 23, 42, 0.45)',
        borderFrost: 'rgba(255, 255, 255, 0.08)'
      },
      fontFamily: {
        sans: ['Inter', 'sans-serif'],
        mono: ['JetBrains Mono', 'monospace'],
      },
    },
  },
  plugins: [],
}
