# ServiceGenie - AI-Powered Commerce Platform

Full-stack MVP for an AI-powered commerce platform with modular architecture, ready for production extension.

## 🏗️ Architecture

### Backend
- **FastAPI** (Python) - RESTful API
- **MongoDB Atlas** - Database
- **Firebase Authentication** - User authentication
- **Cloudinary** - Image storage

### Frontend
- **Next.js 14** (App Router) with TypeScript
- **Firebase Authentication** - Client-side auth
- **Tailwind CSS** - Styling
- **Axios** - API client

## 📁 Project Structure

```
ServiceGenie/
├── backend/          # FastAPI backend
│   ├── app/
│   │   ├── core/     # Configuration, database, Firebase
│   │   ├── models/   # Database models
│   │   ├── schemas/  # Pydantic schemas
│   │   ├── services/ # Business logic
│   │   ├── routes/   # API routes
│   │   ├── utils/    # Utility functions
│   │   └── main.py   # FastAPI app
│   └── requirements.txt
│
└── frontend/         # Next.js frontend
    ├── app/          # Next.js pages
    ├── components/   # React components
    ├── lib/          # Utilities, API client, types
    └── package.json
```

## 🚀 Quick Start

### Backend Setup

1. Navigate to backend directory:
```bash
cd backend
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create `.env` file from `.env.example`:
```bash
cp .env.example .env
```

5. Update `.env` with your credentials:
   - MongoDB Atlas connection string
   - Firebase credentials path
   - Cloudinary credentials (optional)

6. Download Firebase Admin SDK credentials JSON file and place in backend directory.

7. Run the server:
```bash
uvicorn app.main:app --reload
```

Backend will be available at `http://localhost:8000`
API docs at `http://localhost:8000/docs`

### Frontend Setup

1. Navigate to frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Create `.env.local` file from `.env.local.example`:
```bash
cp .env.local.example .env.local
```

4. Update `.env.local` with your Firebase configuration and backend URL.

5. Run the development server:
```bash
npm run dev
```

Frontend will be available at `http://localhost:3000`

## ✨ Features

### For Business Owners
- ✅ Sign up/Login with Firebase Auth
- ✅ Upload product information (name, price, image, category)
- ✅ Manage products (create, read, update, delete)
- ✅ View orders and analytics
- ✅ Chat with AI agent

### For Customers
- ✅ Browse products
- ✅ View product details
- ✅ Place orders
- ✅ Chat with AI agent for product recommendations

### AI Agent
- ✅ Stub implementation ready for OpenAI/Gemini integration
- ✅ Chat interface for both owners and customers
- ✅ Product recommendations based on queries

## 🔑 Environment Variables

### Backend (`.env`)
```
MONGO_URI=mongodb+srv://...
DATABASE_NAME=servicegenie
FIREBASE_PROJECT_ID=your-project-id
FIREBASE_CREDENTIAL_PATH=./firebase-credentials.json
CLOUDINARY_API_KEY=your-key (optional)
CLOUDINARY_API_SECRET=your-secret (optional)
CLOUDINARY_CLOUD_NAME=your-cloud-name (optional)
OPENAI_API_KEY=your-key (optional, for future AI integration)
```

### Frontend (`.env.local`)
```
NEXT_PUBLIC_FIREBASE_API_KEY=your-key
NEXT_PUBLIC_FIREBASE_AUTH_DOMAIN=your-project.firebaseapp.com
NEXT_PUBLIC_FIREBASE_PROJECT_ID=your-project-id
NEXT_PUBLIC_FIREBASE_STORAGE_BUCKET=your-project.appspot.com
NEXT_PUBLIC_FIREBASE_MESSAGING_SENDER_ID=your-sender-id
NEXT_PUBLIC_FIREBASE_APP_ID=your-app-id
NEXT_PUBLIC_BACKEND_URL=http://localhost:8000
```

## 📡 API Endpoints

### Authentication
- `POST /api/v1/auth/verify` - Verify Firebase token
- `GET /api/v1/auth/user/{uid}` - Get user by UID

### Products
- `GET /api/v1/products` - Get all products
- `GET /api/v1/products/{product_id}` - Get product by ID
- `POST /api/v1/products` - Create product (requires auth)
- `PUT /api/v1/products/{product_id}` - Update product (requires auth)
- `DELETE /api/v1/products/{product_id}` - Delete product (requires auth)

### Orders
- `GET /api/v1/orders` - Get orders (requires auth)
- `GET /api/v1/orders/{order_id}` - Get order by ID
- `POST /api/v1/orders` - Create order

### Owners
- `GET /api/v1/owners/me` - Get owner profile (requires auth)
- `POST /api/v1/owners` - Create/update owner profile (requires auth)
- `PUT /api/v1/owners/me` - Update owner profile (requires auth)
- `GET /api/v1/owners/me/analytics` - Get owner analytics (requires auth)

### AI Agent
- `POST /api/v1/agent/chat` - Chat with AI agent
- `GET /api/v1/agent/chat/history` - Get chat history (requires auth)

## 🔧 Development

### Backend
- Add new models in `backend/app/models/`
- Add new schemas in `backend/app/schemas/`
- Add business logic in `backend/app/services/`
- Add new routes in `backend/app/routes/`

### Frontend
- Add new pages in `frontend/app/`
- Add new components in `frontend/components/`
- Update API client in `frontend/lib/api.ts`
- Update types in `frontend/lib/types.ts`

## 🧠 AI Agent Integration

The AI agent service (`backend/app/services/ai_service.py`) is currently a stub implementation. To integrate with OpenAI or Gemini:

1. Install the respective SDK (e.g., `openai`)
2. Update `process_chat_message` function in `ai_service.py`
3. Add API key to backend `.env`

Example OpenAI integration is commented in the service file.

## 📝 Notes

- MongoDB collections are created automatically on first use
- Firebase Authentication handles user management
- Cloudinary is optional - image uploads will fail gracefully if not configured
- AI agent responses are currently keyword-based stubs
- All endpoints return JSON responses
- CORS is configured for localhost development

## 🚢 Production Deployment

1. Update CORS origins in `backend/app/core/config.py`
2. Set proper `SECRET_KEY` in backend `.env`
3. Configure production MongoDB Atlas cluster
4. Set up Firebase production project
5. Configure Cloudinary production account
6. Deploy backend to cloud (e.g., Railway, Render, AWS)
7. Deploy frontend to Vercel or similar
8. Update frontend `.env.local` with production backend URL

## 📄 License

MIT
