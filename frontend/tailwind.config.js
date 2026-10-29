/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        midnight: {
          950: '#060B18',
          900: '#0A1128',
          800: '#0F1A3A',
          700: '#1B2A4A',
          600: '#2C3E6B',
        },
        ivory: {
          50: '#FDFCF9',
          100: '#F9F7F1',
          200: '#F1EFE6',
          300: '#E4E0D2',
          400: '#C8C2AF',
        },
        wanderteal: {
          50: '#F0FDFA',
          100: '#CCFBF1',
          200: '#99F6E4',
          500: '#0D9488',
          600: '#0F766E',
          700: '#115E59',
        },
        sunset: {
          50: '#FFF7ED',
          100: '#FFEDD5',
          500: '#F97316',
          600: '#EA580C',
          700: '#C2410C',
        }
      },
      fontFamily: {
        serif: ['"Playfair Display"', 'Georgia', 'serif'],
        sans: ['"Plus Jakarta Sans"', 'Inter', 'system-ui', 'sans-serif'],
      },
      boxShadow: {
        'soft-sm': '0 2px 8px -2px rgba(10, 17, 40, 0.05)',
        'soft-md': '0 8px 24px -4px rgba(10, 17, 40, 0.08)',
        'soft-lg': '0 16px 36px -6px rgba(10, 17, 40, 0.12)',
        'elevated': '0 20px 45px -10px rgba(10, 17, 40, 0.15)',
      }
    },
  },
  plugins: [],
}
