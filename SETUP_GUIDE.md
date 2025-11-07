# ServiceGenie Setup Guide

Complete step-by-step guide to set up the ServiceGenie MVP.

## Prerequisites

- Node.js 18+ and npm
- Python 3.10+
- MongoDB Atlas account
- Firebase project
- Cloudinary account (optional, for image uploads)

## Step 1: MongoDB Atlas Setup

1. Go to [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
2. Create a free cluster
3. Create a database user (note username and password)
4. Add your IP address to the whitelist (or use 0.0.0.0/0 for development)
5. Get your connection string (replace `<password>` with your password):
   ```
   mongodb+srv://<username>:<password>@cluster.mongodb.net/?retryWrites=true&w=majority
   ```

## Step 2: Firebase Setup

1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Create a new project (or use existing)
3. Enable Authentication:
   - Go to Authentication > Sign-in method
   - Enable Email/Password
4. Get Web App configuration:
   - Go to Project Settings > General
   - Scroll down to "Your apps"
   - Click the web icon (`</>`) to add a web app
   - Copy the Firebase configuration object
5. Download Service Account Key:
   - Go to Project Settings > Service Accounts
   - Click "Generate new private key"
   - Save the JSON file as `firebase-credentials.json` in the `backend` folder

## Step 3: Cloudinary Setup (Optional)

1. Go to [Cloudinary](https://cloudinary.com/)
2. Sign up for a free account
3. Go to Dashboard
4. Copy your:
   - Cloud Name
   - API Key
   - API Secret

## Step 4: Backend Setup

1. Navigate to backend directory:
```bash
cd backend
```

2. Create virtual environment:
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create `.env` file:
```bash
# Windows
copy .env.example .env

# macOS/Linux
cp .env.example .env
```

5. Edit `.env` file with your credentials:
```env
MONGO_URI=mongodb+srv://username:password@cluster.mongodb.net/?retryWrites=true&w=majority
DATABASE_NAME=servicegenie

FIREBASE_PROJECT_ID=your-firebase-project-id
FIREBASE_CREDENTIAL_PATH=./firebase-credentials.json

CLOUDINARY_API_KEY=your-cloudinary-api-key
CLOUDINARY_API_SECRET=your-cloudinary-api-secret
CLOUDINARY_CLOUD_NAME=your-cloudinary-cloud-name

OPENAI_API_KEY=your-openai-api-key
API_V1_PREFIX=/api/v1
SECRET_KEY=dev-secret-key-change-in-production
ENVIRONMENT=development
ALLOWED_ORIGINS=["http://localhost:3000","http://localhost:3001"]
```

6. Place `firebase-credentials.json` in the backend directory.

7. Run the backend:
```bash
uvicorn app.main:app --reload
```

The backend should be running at `http://localhost:8000`
API documentation at `http://localhost:8000/docs`

## Step 5: Frontend Setup

1. Navigate to frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Create `.env.local` file:
```bash
# Windows
copy .env.local.example .env.local

# macOS/Linux
cp .env.local.example .env.local
```

4. Edit `.env.local` with your Firebase configuration:
```env
NEXT_PUBLIC_FIREBASE_API_KEY=your-firebase-api-key
NEXT_PUBLIC_FIREBASE_AUTH_DOMAIN=your-project.firebaseapp.com
NEXT_PUBLIC_FIREBASE_PROJECT_ID=your-firebase-project-id
NEXT_PUBLIC_FIREBASE_STORAGE_BUCKET=your-project.appspot.com
NEXT_PUBLIC_FIREBASE_MESSAGING_SENDER_ID=your-messaging-sender-id
NEXT_PUBLIC_FIREBASE_APP_ID=your-app-id

NEXT_PUBLIC_BACKEND_URL=http://localhost:8000
```

5. Run the frontend:
```bash
npm run dev
```

The frontend should be running at `http://localhost:3000`

## Step 6: Testing the Setup

1. Open `http://localhost:3000` in your browser
2. Click "Register" to create an account
3. Login with your credentials
4. You should be redirected to the dashboard
5. Try creating a product
6. Test the chat functionality

## Troubleshooting

### Backend Issues

**MongoDB Connection Error:**
- Check your connection string in `.env`
- Verify your IP is whitelisted in MongoDB Atlas
- Check if your username/password are correct

**Firebase Error:**
- Verify `firebase-credentials.json` is in the backend directory
- Check the file path in `.env` matches the actual file location
- Ensure Firebase project ID matches in `.env`

**Import Errors:**
- Make sure virtual environment is activated
- Reinstall dependencies: `pip install -r requirements.txt`

### Frontend Issues

**Firebase Auth Error:**
- Verify all Firebase environment variables are set in `.env.local`
- Check Firebase project settings
- Ensure Email/Password authentication is enabled

**API Connection Error:**
- Verify backend is running on `http://localhost:8000`
- Check `NEXT_PUBLIC_BACKEND_URL` in `.env.local`
- Check browser console for CORS errors

**Build Errors:**
- Delete `node_modules` and `package-lock.json`
- Run `npm install` again
- Check Node.js version (should be 18+)

## Next Steps

1. **Customize the AI Agent:**
   - Edit `backend/app/services/ai_service.py`
   - Integrate OpenAI or Gemini API
   - Update `OPENAI_API_KEY` in `.env`

2. **Add More Features:**
   - Payment integration (Stripe)
   - Email notifications
   - Advanced analytics
   - Product search and filters

3. **Deploy to Production:**
   - Deploy backend to Railway, Render, or AWS
   - Deploy frontend to Vercel or Netlify
   - Update environment variables
   - Configure production MongoDB cluster
   - Set up production Firebase project

## Support

For issues or questions, please check:
- Backend README: `backend/README.md`
- Frontend README: `frontend/README.md`
- Main README: `README.md`

