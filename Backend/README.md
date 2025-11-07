# ServiceGenie Backend

Backend API for ServiceGenie - AI-powered commerce platform.

## Tech Stack

- **FastAPI** (Python)
- **MongoDB Atlas** (via Motor)
- **Firebase Authentication**
- **Cloudinary** (for image storage)

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Copy `.env.example` to `.env` and fill in your credentials:
```bash
cp .env.example .env
```

4. Update `.env` with:
   - MongoDB Atlas connection string
   - Firebase credentials path
   - Cloudinary credentials (optional)
   - OpenAI API key (optional, for future AI integration)

5. Download Firebase credentials JSON file and place it in the backend directory.

## Running the Application

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`.
API documentation (Swagger) will be available at `http://localhost:8000/docs`.

## API Endpoints

### Authentication
- `POST /api/v1/auth/verify` - Verify Firebase token
- `GET /api/v1/auth/user/{uid}` - Get user by UID

### Products
- `GET /api/v1/products` - Get all products
- `GET /api/v1/products/{product_id}` - Get product by ID
- `POST /api/v1/products` - Create product
- `PUT /api/v1/products/{product_id}` - Update product
- `DELETE /api/v1/products/{product_id}` - Delete product

### Orders
- `GET /api/v1/orders` - Get orders
- `GET /api/v1/orders/{order_id}` - Get order by ID
- `POST /api/v1/orders` - Create order

### Owners
- `GET /api/v1/owners/me` - Get owner profile
- `POST /api/v1/owners` - Create/update owner profile
- `PUT /api/v1/owners/me` - Update owner profile
- `GET /api/v1/owners/me/analytics` - Get owner analytics

### AI Agent
- `POST /api/v1/agent/chat` - Chat with AI agent
- `GET /api/v1/agent/chat/history` - Get chat history

## Project Structure

```
backend/
├── app/
│   ├── core/        # Configuration and database
│   ├── models/      # Database models
│   ├── schemas/     # Pydantic schemas
│   ├── services/    # Business logic
│   ├── routes/      # API routes
│   ├── utils/       # Utility functions
│   └── main.py      # FastAPI application
└── requirements.txt
```

## Development

The backend is structured for easy extension:
- Add new models in `app/models/`
- Add new schemas in `app/schemas/`
- Add business logic in `app/services/`
- Add new routes in `app/routes/`

AI agent service is currently a stub implementation. Replace `process_chat_message` in `app/services/ai_service.py` with actual AI integration (OpenAI, Gemini, etc.).
