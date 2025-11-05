# ServiceGenie - Getting Started

Welcome to ServiceGenie! This guide will help you set up and run the project.

## Prerequisites

Make sure you have the following installed:

- **Node.js** 18+ ([Download](https://nodejs.org/))
- **Python** 3.9+ ([Download](https://www.python.org/))
- **MongoDB** ([Download](https://www.mongodb.com/try/download/community))
- **Git** ([Download](https://git-scm.com/))

## Quick Setup

### Option 1: Automated Setup (Recommended)

#### On Linux/Mac:
```bash
chmod +x quick-start.sh
./quick-start.sh
```

#### On Windows:
```bash
quick-start.bat
```

### Option 2: Manual Setup

#### 1. Backend Setup

```bash
# Navigate to backend
cd Backend

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Setup environment
cp .env.example .env
# Edit .env with your configuration

# Seed database (optional)
python scripts/seed_db.py

# Run backend
uvicorn main:app --reload
```

Backend runs on: http://localhost:8000

#### 2. Frontend Setup

```bash
# Navigate to frontend (new terminal)
cd Frontend

# Install dependencies
npm install

# Setup environment
cp .env.example .env.local
# Edit .env.local with your configuration

# Run frontend
npm run dev
```

Frontend runs on: http://localhost:3000

## Configuration

### Backend (.env)

```env
# MongoDB
MONGODB_URL=mongodb://localhost:27017
DATABASE_NAME=servicegenie

# Firebase - Get from Firebase Console
FIREBASE_CREDENTIALS_PATH=./firebase-credentials.json

# API Security
SECRET_KEY=your-secret-key-min-32-characters
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS
ALLOWED_ORIGINS=http://localhost:3000

# Stripe - Get from Stripe Dashboard
STRIPE_SECRET_KEY=sk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...

# Environment
ENVIRONMENT=development
```

### Frontend (.env.local)

```env
# Backend API
NEXT_PUBLIC_API_URL=http://localhost:8000/api

# Firebase - Get from Firebase Console (Project Settings > Your Apps)
NEXT_PUBLIC_FIREBASE_API_KEY=AIzaSy...
NEXT_PUBLIC_FIREBASE_AUTH_DOMAIN=your-app.firebaseapp.com
NEXT_PUBLIC_FIREBASE_PROJECT_ID=your-project-id
NEXT_PUBLIC_FIREBASE_STORAGE_BUCKET=your-app.appspot.com
NEXT_PUBLIC_FIREBASE_MESSAGING_SENDER_ID=123456789
NEXT_PUBLIC_FIREBASE_APP_ID=1:123456789:web:abcdef

# Stripe - Get from Stripe Dashboard
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=pk_test_...
```

## Firebase Setup

1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Create a new project or select existing
3. Enable Authentication:
   - Go to Build > Authentication
   - Enable Email/Password and Google sign-in
4. Get Web App credentials:
   - Project Settings > Your Apps > Add Web App
   - Copy configuration to `.env.local`
5. Get Admin SDK credentials:
   - Project Settings > Service Accounts
   - Generate new private key
   - Save as `Backend/firebase-credentials.json`

## Stripe Setup

1. Go to [Stripe Dashboard](https://dashboard.stripe.com/)
2. Create account or login
3. Get API keys:
   - Developers > API Keys
   - Copy Publishable key to frontend `.env.local`
   - Copy Secret key to backend `.env`
4. Setup webhooks (for production):
   - Developers > Webhooks
   - Add endpoint: `https://your-domain.com/api/payment/webhook`
   - Select events: `payment_intent.succeeded`, `payment_intent.payment_failed`

## MongoDB Setup

### Local MongoDB

```bash
# Start MongoDB
mongod

# Or on Linux/Mac with service:
sudo systemctl start mongod

# Or on Windows:
# Start MongoDB service from Services
```

### MongoDB Atlas (Cloud)

1. Go to [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
2. Create free cluster
3. Get connection string
4. Update `MONGODB_URL` in backend `.env`

## Running the Application

### Development Mode

Terminal 1 (Backend):
```bash
cd Backend
source venv/bin/activate  # Windows: venv\Scripts\activate
uvicorn main:app --reload
```

Terminal 2 (Frontend):
```bash
cd Frontend
npm run dev
```

### Access the Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

## Default Test Data

If you ran the seed script, you'll have:
- 6 Categories (Electronics, Fashion, Watches, Audio, Home & Living, Gifts)
- 8 Sample Products with images and details

## Common Issues

### MongoDB Connection Error
- Make sure MongoDB is running
- Check `MONGODB_URL` in `.env`
- Test connection: `mongosh` or `mongo`

### Firebase Auth Error
- Verify Firebase credentials are correct
- Check `firebase-credentials.json` exists
- Enable Email/Password in Firebase Console

### Port Already in Use
- Backend: Change port in command: `uvicorn main:app --reload --port 8001`
- Frontend: Change port: `npm run dev -- -p 3001`

### Dependencies Not Installing
- Python: Try `pip install --upgrade pip` then reinstall
- Node: Try `npm cache clean --force` then reinstall

## Next Steps

1. Create an admin user for product management
2. Configure Stripe for payments
3. Customize theme colors in `tailwind.config.ts`
4. Add more products via API or admin panel
5. Test the complete shopping flow

## Support

- Check [Backend README](./Backend/README.md) for API details
- Check [Frontend README](./Frontend/README.md) for UI details
- Open an issue on GitHub for bugs
- See main [README](./README.md) for architecture

## Development Tips

- Use API docs at `/docs` to test endpoints
- Frontend hot-reloads on code changes
- Backend auto-reloads with `--reload` flag
- Check browser console for frontend errors
- Check terminal for backend errors

Happy coding! 🚀
