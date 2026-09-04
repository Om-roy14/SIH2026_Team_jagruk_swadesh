/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        nature: {
          950: '#07150b',
          900: '#0d2113',
          850: '#132c1b',
          800: '#1b3824',
          700: '#264b32',
          600: '#346142',
          500: '#467a55',
        },
        forest: {
          dark: '#08170c',
          deep: '#112516',
          card: '#18311e',
          olive: '#23442a',
          sage: '#486851',
          accent: '#5e8567',
        },
        saffron: {
          DEFAULT: '#E8a317',
          hover: '#D99200',
          light: '#F5C453',
          dark: '#B87200',
          glow: 'rgba(232, 163, 23, 0.25)',
        },
        ivory: {
          DEFAULT: '#F4F7F2',
          muted: '#D2DAD0',
          dim: '#9EB09E',
          warm: '#FAFBF8',
        }
      },
      fontFamily: {
        sans: ['"Manrope"', 'Inter', 'system-ui', 'sans-serif'],
      },
      backdropBlur: {
        'liquid': '16px',
        'liquid-heavy': '24px',
      },
      boxShadow: {
        'liquid': '0 12px 35px -8px rgba(3, 14, 7, 0.4), inset 0 1px 1px rgba(255, 255, 255, 0.15)',
        'liquid-hover': '0 18px 45px -8px rgba(3, 14, 7, 0.55), inset 0 1px 1.5px rgba(255, 255, 255, 0.25)',
        'pill-primary': '0 8px 20px -4px rgba(7, 24, 12, 0.5), inset 0 1px 1px rgba(255, 255, 255, 0.2)',
      },
      backgroundImage: {
        'liquid-gradient': 'linear-gradient(140deg, rgba(35, 68, 42, 0.75) 0%, rgba(13, 33, 19, 0.85) 100%)',
        'pill-primary-gradient': 'linear-gradient(135deg, #1d3823 0%, #112416 100%)',
      }
    },
  },
  plugins: [],
}

