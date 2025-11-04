# ServiceGenie - AI-Powered E-Commerce Platform

ServiceGenie is a modern, full-stack e-commerce platform with AI capabilities, built for seamless online shopping experiences.

## 🌟 Features

### For Customers
- 🛍️ Browse products by categories
- 🔍 Advanced search and filtering
- 🛒 Shopping cart management
- 💳 Secure payment processing (Stripe)
- 📦 Order tracking
- 👤 User authentication (Email/Google)
- 📱 Fully responsive design
- 🎨 Beautiful royal blue & black theme

### For Admins
- 📊 Product management (CRUD)
- 📁 Category management
- 📦 Order management
- 👥 User management
- 💰 Sales analytics (coming soon)
- 🤖 AI assistant integration (roadmap)

## 🏗️ Architecture

```
ServiceGenie/
├── Frontend/          # Next.js 14 application
│   ├── src/
│   │   ├── app/      # App Router pages
│   │   ├── components/
│   │   ├── lib/      # Utilities
│   │   └── types/    # TypeScript types
│   └── public/
│
└── Backend/          # FastAPI application
    ├── app/
    │   ├── api/      # API routes
    │   ├── core/     # Core configs
    │   └── models/   # Data models
    └── main.py
```

## 🚀 Tech Stack

### Frontend
- **Framework**: Next.js 14 (App Router)
- **Language**: TypeScript
- **Styling**: TailwindCSS
- **State**: React Context + Zustand
- **Auth**: Firebase Authentication
- **Payments**: Stripe
- **Icons**: Lucide React
- **Animations**: Framer Motion

### Backend
- **Framework**: FastAPI
- **Language**: Python 3.9+
- **Database**: MongoDB
- **Auth**: Firebase Admin SDK
- **Payments**: Stripe
- **Async Driver**: Motor

## 📋 Prerequisites

Before you begin, ensure you have:
- Node.js 18+ and npm/yarn
- Python 3.9+
- MongoDB (local or cloud instance)
- Firebase project
- Stripe account

## 🛠️ Installation

### 1. Clone the Repository
```bash
git clone https://github.com/codenim34/ServiceGenie.git
cd ServiceGenie
```

### 2. Backend Setup

```bash
cd Backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your configuration

# Add Firebase credentials
# Download firebase-credentials.json from Firebase Console
# Place it in Backend directory

# Seed database with sample data
python scripts/seed_db.py

# Run the server
uvicorn main:app --reload --port 8000
```

Backend will run on: `http://localhost:8000`

API Docs: `http://localhost:8000/docs`

### 3. Frontend Setup

```bash
cd Frontend

# Install dependencies
npm install
# or
yarn install

# Configure environment
cp .env.example .env.local
# Edit .env.local with your configuration

# Run development server
npm run dev
# or
yarn dev
```

Frontend will run on: `http://localhost:3000`

## 🔐 Environment Configuration

### Backend (.env)
```env
MONGODB_URL=mongodb://localhost:27017
DATABASE_NAME=servicegenie
FIREBASE_CREDENTIALS_PATH=./firebase-credentials.json
SECRET_KEY=your-secret-key-change-this
ALLOWED_ORIGINS=http://localhost:3000
STRIPE_SECRET_KEY=sk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...
```

### Frontend (.env.local)
```env
NEXT_PUBLIC_API_URL=http://localhost:8000/api
NEXT_PUBLIC_FIREBASE_API_KEY=...
NEXT_PUBLIC_FIREBASE_AUTH_DOMAIN=...
NEXT_PUBLIC_FIREBASE_PROJECT_ID=...
NEXT_PUBLIC_FIREBASE_STORAGE_BUCKET=...
NEXT_PUBLIC_FIREBASE_MESSAGING_SENDER_ID=...
NEXT_PUBLIC_FIREBASE_APP_ID=...
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=pk_test_...
```

## 🎨 Theme

ServiceGenie uses a royal blue and black gradient theme:
- **Primary**: Royal Blue (#0047e6)
- **Dark Tones**: Pure Black to Dark Blue
- **Accents**: Gradient overlays with glass morphism
- **Effects**: Shimmer animations, backdrop blur

## 📱 Quick Start Guide

1. **Start MongoDB**: Make sure MongoDB is running
2. **Start Backend**: `cd Backend && uvicorn main:app --reload`
3. **Seed Database**: `python scripts/seed_db.py` (optional)
4. **Start Frontend**: `cd Frontend && npm run dev`
5. **Access Application**: Open `http://localhost:3000`

## 🔌 API Documentation

Full API documentation available at `http://localhost:8000/docs` when backend is running.

Key endpoints:
- `/api/products` - Product management
- `/api/categories` - Category management
- `/api/orders` - Order management
- `/api/users` - User management
- `/api/payment` - Payment processing

## 📦 Deployment

### Backend (Production)
```bash
# Using Gunicorn + Uvicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### Frontend (Vercel)
```bash
# Build
npm run build

# Or deploy to Vercel
vercel deploy --prod
```

## 🔮 Roadmap

- [x] Core e-commerce functionality
- [x] Firebase authentication
- [x] Stripe payment integration
- [x] Product management
- [x] Order management
- [x] Royal blue theme
- [ ] AI chatbot assistant
- [ ] Advanced analytics dashboard
- [ ] Multi-language support (Bangla, Banglish)
- [ ] Image-based product search
- [ ] Recommendation engine
- [ ] Email notifications
- [ ] Review and rating system
- [ ] Wishlist functionality

## 📄 License

Proprietary - ServiceGenie © 2025

## 👥 Team

- **Codenim34** - [GitHub](https://github.com/codenim34)

---

**Made with ❤️ for seamless e-commerce experiences**