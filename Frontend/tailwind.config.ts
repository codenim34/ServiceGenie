import type { Config } from 'tailwindcss'

const config: Config = {
  content: [
    './src/pages/**/*.{js,ts,jsx,tsx,mdx}',
    './src/components/**/*.{js,ts,jsx,tsx,mdx}',
    './src/app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#e6eeff',
          100: '#b3ccff',
          200: '#80aaff',
          300: '#4d88ff',
          400: '#1a66ff',
          500: '#0047e6',  // Royal Blue
          600: '#0037b3',
          700: '#002780',
          800: '#00174d',
          900: '#00071a',
        },
        dark: {
          50: '#1a1a2e',
          100: '#16213e',
          200: '#0f1419',
          300: '#0a0e27',
          400: '#05091a',
          500: '#000000',
        }
      },
      backgroundImage: {
        'gradient-radial': 'radial-gradient(var(--tw-gradient-stops))',
        'gradient-royal': 'linear-gradient(135deg, #0047e6 0%, #000000 100%)',
        'gradient-royal-dark': 'linear-gradient(135deg, #002780 0%, #000000 100%)',
        'gradient-shimmer': 'linear-gradient(90deg, transparent, rgba(0, 71, 230, 0.3), transparent)',
      },
      animation: {
        'shimmer': 'shimmer 2s infinite',
        'fade-in': 'fadeIn 0.5s ease-in',
        'slide-up': 'slideUp 0.5s ease-out',
      },
      keyframes: {
        shimmer: {
          '0%': { transform: 'translateX(-100%)' },
          '100%': { transform: 'translateX(100%)' },
        },
        fadeIn: {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' },
        },
        slideUp: {
          '0%': { transform: 'translateY(20px)', opacity: '0' },
          '100%': { transform: 'translateY(0)', opacity: '1' },
        },
      },
    },
  },
  plugins: [],
}
export default config
