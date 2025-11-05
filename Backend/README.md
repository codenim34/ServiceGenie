# ServiceGenie Backend

AI-powered e-commerce platform backend built with FastAPI and MongoDB.

## Features

- 🔐 Firebase Authentication integration
- 🛍️ Product management with categories
- 🛒 Order management system
- 💳 Stripe payment integration
- 📊 MongoDB database
- 🚀 FastAPI async endpoints
- 🔒 Role-based access control (Admin/Customer)

## Tech Stack

- **Framework**: FastAPI
- **Database**: MongoDB (Motor async driver)
- **Authentication**: Firebase Admin SDK
- **Payment**: Stripe
- **Python**: 3.9+

## Setup

### Prerequisites

- Python 3.9 or higher
- MongoDB installed and running
- Firebase project with Admin SDK credentials
- Stripe account for payment processing

### Installation

1. **Create virtual environment**:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Environment Configuration**:
```bash
cp .env.example .env
```

Edit `.env` and add your configuration:
- MongoDB connection URL
- Firebase credentials path
- Stripe API keys
- Secret key for JWT

4. **Firebase Setup**:
   - Follow the [Firebase Setup Guide](FIREBASE_SETUP.md) for detailed instructions
   - Download your Firebase Admin SDK JSON file from Firebase Console
   - Save it as `firebase-credentials.json` in the Backend directory
   - Update `FIREBASE_CREDENTIALS_PATH` in `.env`

5. **Test Connections**:
```bash
# Test MongoDB connection
python tests/test_db_connection.py

# Test Firebase connection
python tests/test_firebase_connection.py
```

6. **Seed Database (Optional)**:
```bash
python scripts/seed_db.py
```

7. **Run the application**:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at: `http://localhost:8000`

API Documentation: `http://localhost:8000/docs`

## API Endpoints

### Authentication
- All protected endpoints require Firebase ID token in Authorization header
- Format: `Authorization: Bearer <firebase-id-token>`

### Users
- `POST /api/users/sync` - Sync user from Firebase
- `GET /api/users/me` - Get current user
- `PUT /api/users/me` - Update current user

### Products
- `GET /api/products` - Get all products (with filters)
- `GET /api/products/{id}` - Get single product
- `POST /api/products` - Create product (Admin)
- `PUT /api/products/{id}` - Update product (Admin)
- `DELETE /api/products/{id}` - Delete product (Admin)

### Categories
- `GET /api/categories` - Get all categories
- `GET /api/categories/{id}` - Get single category
- `POST /api/categories` - Create category (Admin)
- `PUT /api/categories/{id}` - Update category (Admin)
- `DELETE /api/categories/{id}` - Delete category (Admin)

### Orders
- `POST /api/orders` - Create order
- `GET /api/orders` - Get user's orders
- `GET /api/orders/all` - Get all orders (Admin)
- `GET /api/orders/{id}` - Get single order
- `PUT /api/orders/{id}` - Update order status (Admin)
- `DELETE /api/orders/{id}` - Cancel order

### Payment
- `POST /api/payment/create-payment-intent` - Create Stripe payment intent
- `POST /api/payment/webhook` - Stripe webhook handler

## Database Schema

### Collections

#### users
```json
{
  "_id": "ObjectId",
  "uid": "firebase-uid",
  "email": "user@example.com",
  "displayName": "John Doe",
  "photoURL": "https://...",
  "role": "customer|admin",
  "createdAt": "ISO Date",
  "updatedAt": "ISO Date"
}
```

#### products
```json
{
  "_id": "ObjectId",
  "name": "Product Name",
  "description": "Description",
  "price": 99.99,
  "originalPrice": 149.99,
  "discount": 33.33,
  "category": "electronics",
  "images": ["url1", "url2"],
  "stock": 50,
  "rating": 4.5,
  "reviews": 120,
  "tags": ["tag1", "tag2"],
  "specifications": {"key": "value"},
  "featured": true,
  "createdAt": "ISO Date",
  "updatedAt": "ISO Date"
}
```

#### orders
```json
{
  "_id": "ObjectId",
  "userId": "firebase-uid",
  "items": [
    {
      "productId": "ObjectId",
      "name": "Product Name",
      "price": 99.99,
      "quantity": 2,
      "image": "url"
    }
  ],
  "totalAmount": 199.98,
  "status": "pending|processing|shipped|delivered|cancelled",
  "paymentStatus": "pending|paid|failed",
  "paymentMethod": "stripe",
  "shippingAddress": {
    "name": "John Doe",
    "phone": "+123456789",
    "address": "123 Main St",
    "city": "City",
    "postalCode": "12345",
    "country": "Country"
  },
  "createdAt": "ISO Date",
  "updatedAt": "ISO Date"
}
```

## Security

- Firebase ID tokens are verified on each request
- Admin-only endpoints check user role
- CORS configured for frontend origin
- MongoDB queries use ObjectId validation
- Stripe webhook signatures are verified

## Project Structure

```
Backend/
├── app/                      # Application code
│   ├── api/                  # API routes
│   │   └── v1/              # API version 1
│   │       ├── api.py       # Router aggregator
│   │       └── endpoints/   # Individual endpoint modules
│   ├── core/                # Core functionality
│   │   ├── config.py        # Settings & configuration
│   │   ├── database.py      # Database connection
│   │   ├── firebase.py      # Firebase Admin SDK
│   │   └── security.py      # Auth & security
│   └── models/              # Data models (Pydantic)
├── scripts/                 # Utility scripts
│   └── seed_db.py          # Database seeding
├── tests/                   # Test suite
│   ├── test_api.py         # API endpoint tests
│   ├── test_db_connection.py  # Database connection test
│   └── test_firebase_connection.py  # Firebase connection test
├── main.py                  # Application entry point
├── requirements.txt         # Python dependencies
└── .env                     # Environment variables (gitignored)
```

See [STRUCTURE.md](STRUCTURE.md) for detailed architecture and best practices.

## Development

```bash
# Run with auto-reload
uvicorn main:app --reload

# Run with specific port
uvicorn main:app --port 8080

# Run in production
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

## Documentation

- [Setup Guide](SETUP_GUIDE.md) - Comprehensive setup instructions
- [Firebase Setup](FIREBASE_SETUP.md) - Firebase configuration guide
- [Structure Guide](STRUCTURE.md) - Code organization and best practices
- [API Documentation](http://localhost:8000/docs) - Interactive Swagger UI

## Testing

### Connection Tests
```bash
# Test MongoDB connection
python tests/test_db_connection.py

# Test Firebase connection
python tests/test_firebase_connection.py
```

### Unit Tests
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app tests/
```

### API Testing
Test the API using:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`
- Postman/Thunder Client

## Deployment

For production deployment:

1. Set `ENVIRONMENT=production` in `.env`
2. Use a production MongoDB instance
3. Configure proper CORS origins
4. Set up SSL/TLS certificates
5. Use a production WSGI server (Gunicorn + Uvicorn workers)
6. Enable Stripe webhook endpoints

## License

Proprietary - ServiceGenie
