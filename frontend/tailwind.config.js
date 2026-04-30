/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        cpi: {
          // Primary Blues
          blue: {
            DEFAULT: '#0058AA',
            50: '#E7EDF2',
            100: '#e0e9f7',
            200: '#0072dd',
            300: '#006fa0',
            400: '#0058AA',
            500: '#004E98',
            600: '#003E77',
            700: '#002F58',
            800: '#001d38',
            900: '#00172b',
          },
          // Alert Colors
          red: {
            DEFAULT: '#d3353d',
            light: '#dc5f65',
            dark: '#af262d',
            bg: '#F6E5E5',
          },
          orange: {
            DEFAULT: '#ff9200',
            light: '#ffbe66',
            bg: '#fefbf3',
          },
          teal: {
            DEFAULT: '#007169',
          },
        },
      },
      fontFamily: {
        sans: ['Inter', 'Helvetica Neue', 'Arial', 'sans-serif'],
        mono: ['Roboto Mono', 'Courier New', 'monospace'],
      },
    },
  },
  plugins: [],
}