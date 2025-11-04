# ServiceGenie Frontend

AI-powered e-commerce platform frontend built with Next.js 14 App Router and TailwindCSS.

## Features

- 🎨 Royal Blue & Black gradient theme
- 🔐 Firebase Authentication (Email/Password & Google)
- 🛍️ Product browsing with categories
- 🛒 Shopping cart functionality
- 💳 Stripe payment integration
- 📱 Fully responsive design
- ⚡ Fast and optimized with Next.js 14
- 🎭 Beautiful animations with Framer Motion
- 🔍 Product search and filtering

## Tech Stack

- **Framework**: Next.js 14 (App Router)
- **Styling**: TailwindCSS
- **Authentication**: Firebase Auth
- **State Management**: Zustand & React Context
- **HTTP Client**: Axios
- **UI Components**: Lucide React Icons
- **Animations**: Framer Motion
- **Payments**: Stripe

## Setup

### Prerequisites

- Node.js 18+ and npm/yarn
- Firebase project with Web App configured
- Stripe publishable key

### Installation

1. **Install dependencies**:
```bash
cd Frontend
npm install
# or
yarn install
```

2. **Environment Configuration**:
```bash
cp .env.example .env.local
```

Edit `.env.local` and add your configuration:

```env
# Backend API
NEXT_PUBLIC_API_URL=http://localhost:8000/api

# Firebase Configuration
NEXT_PUBLIC_FIREBASE_API_KEY=your_api_key
NEXT_PUBLIC_FIREBASE_AUTH_DOMAIN=your_project.firebaseapp.com
NEXT_PUBLIC_FIREBASE_PROJECT_ID=your_project_id
NEXT_PUBLIC_FIREBASE_STORAGE_BUCKET=your_project.appspot.com
NEXT_PUBLIC_FIREBASE_MESSAGING_SENDER_ID=your_sender_id
NEXT_PUBLIC_FIREBASE_APP_ID=your_app_id

# Stripe
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=pk_test_...
```

3. **Firebase Setup**:
   - Go to Firebase Console
   - Create a new project or use existing
   - Enable Authentication (Email/Password and Google)
   - Get your Web App configuration
   - Add configuration to `.env.local`

4. **Run development server**:
```bash
npm run dev
# or
yarn dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

## Project Structure

```
Frontend/
├── src/
│   ├── app/              # Next.js 14 App Router pages
│   │   ├── layout.tsx    # Root layout
│   │   ├── page.tsx      # Home page
│   │   ├── globals.css   # Global styles
│   │   ├── products/     # Products pages
│   │   ├── cart/         # Cart page
│   │   ├── checkout/     # Checkout page
│   │   └── auth/         # Auth pages
│   ├── components/       # React components
│   │   ├── layout/       # Header, Footer
│   │   ├── home/         # Home page components
│   │   ├── products/     # Product components
│   │   └── Providers.tsx # Context providers
│   ├── lib/              # Utilities and configs
│   │   ├── api/          # API client
│   │   ├── auth/         # Auth context
│   │   ├── store/        # State management
│   │   └── firebase/     # Firebase config
│   └── types/            # TypeScript types
├── public/               # Static assets
├── package.json
├── tsconfig.json
├── tailwind.config.ts
└── next.config.js
```

## Features in Detail

### Theme
- **Primary Color**: Royal Blue (#0047e6)
- **Background**: Black to Royal Blue gradient
- **Glass Effect**: Backdrop blur with border
- **Animations**: Shimmer, fade-in, slide-up

### Authentication
- Email/Password signup and login
- Google OAuth sign-in
- Password reset functionality
- Protected routes
- User profile management

### Shopping Experience
- Product grid with filters
- Category-based browsing
- Product detail pages
- Add to cart functionality
- Cart management
- Checkout process
- Order history

### Responsive Design
- Mobile-first approach
- Tablet and desktop optimized
- Touch-friendly interfaces
- Accessible components

## Available Scripts

```bash
# Development
npm run dev

# Build for production
npm run build

# Start production server
npm run start

# Lint code
npm run lint
```

## Environment Variables

All environment variables must be prefixed with `NEXT_PUBLIC_` to be accessible in the browser.

Required variables:
- `NEXT_PUBLIC_API_URL`: Backend API URL
- `NEXT_PUBLIC_FIREBASE_*`: Firebase configuration
- `NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY`: Stripe key

## Deployment

### Vercel (Recommended)

1. Push code to GitHub
2. Import project to Vercel
3. Add environment variables
4. Deploy

### Manual Deployment

```bash
npm run build
npm run start
```

Use a process manager like PM2:
```bash
pm2 start npm --name "servicegenie-frontend" -- start
```

## API Integration

The frontend communicates with the FastAPI backend through the API client (`src/lib/api/client.ts`).

All authenticated requests include the Firebase ID token:
```
Authorization: Bearer <firebase-id-token>
```

## Theme Customization

Edit `tailwind.config.ts` to customize:
- Colors
- Gradients
- Animations
- Breakpoints

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)
- Mobile browsers

## Performance

- Code splitting with Next.js
- Image optimization with next/image
- Lazy loading of components
- Caching strategies
- Optimized bundle size

## License

Proprietary - ServiceGenie
