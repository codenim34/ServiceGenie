# Quick Testing Guide

## 🧪 Testing Your ServiceGenie Backend

### Step-by-Step Testing Process

#### 1️⃣ Test MongoDB Connection

```bash
cd Backend
python tests/test_db_connection.py
```

**Expected Output:**
```
✅ Connection successful! MongoDB is responding
✅ Database 'ServiceGenie' accessible
✅ Write operation successful
✅ Read operation successful
✅ Cleanup completed
```

**Troubleshooting:**
- ❌ Connection failed → Check `MONGODB_URL` in `.env`
- ❌ Database error → Verify database name matches (case-sensitive)
- ❌ Timeout → Check internet connection and MongoDB Atlas IP whitelist

---

#### 2️⃣ Test Firebase Connection

**Before Testing:**
1. Download Firebase credentials from [Firebase Console](https://console.firebase.google.com/)
2. Save as `Backend/firebase-credentials.json`
3. Add to `.env`: `FIREBASE_CREDENTIALS_PATH=firebase-credentials.json`

```bash
python tests/test_firebase_connection.py
```

**Expected Output:**
```
✅ Credentials file found
✅ Credentials file format is valid
✅ Firebase Admin SDK initialized successfully
✅ Firebase Authentication is working!
✅ Token verification function is available
✅ Custom token created for test user
```

**Troubleshooting:**
- ❌ Credentials file not found → Check path in `.env`
- ❌ Invalid credentials → Re-download from Firebase Console
- ❌ Permission denied → Verify Firebase project is active
- ❌ Network error → Check firewall/internet connection

See [FIREBASE_SETUP.md](FIREBASE_SETUP.md) for detailed Firebase setup guide.

---

#### 3️⃣ Run Unit Tests

```bash
# Install testing dependencies if not already installed
pip install -r requirements.txt

# Run all tests
pytest

# Run with verbose output
pytest -v

# Run with coverage report
pytest --cov=app tests/
```

---

#### 4️⃣ Test API Endpoints

**Start the Server:**
```bash
uvicorn main:app --reload
```

**Access API Documentation:**
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

**Test Endpoints:**

1. **Health Check (No Auth Required):**
   ```bash
   curl http://localhost:8000/
   ```

2. **Get Categories (No Auth Required):**
   ```bash
   curl http://localhost:8000/api/v1/categories
   ```

3. **Get Products (No Auth Required):**
   ```bash
   curl http://localhost:8000/api/v1/products
   ```

4. **Protected Endpoints (Auth Required):**
   - Get current user profile
   - Create order
   - Update user info
   
   You'll need a Firebase ID token from your frontend auth.

---

#### 5️⃣ Seed Database (Optional)

Populate database with sample data:

```bash
python scripts/seed_db.py
```

**Sample Data Includes:**
- 6 Categories (Electronics, Fashion, Home & Garden, etc.)
- 8 Products (with images, prices, ratings)

---

## ✅ Testing Checklist

Use this checklist to verify your setup:

- [ ] Python virtual environment activated
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] `.env` file created and configured
- [ ] MongoDB connection test passed
- [ ] Firebase credentials downloaded and configured
- [ ] Firebase connection test passed
- [ ] API server starts without errors
- [ ] API documentation accessible at `/docs`
- [ ] Database seeded with sample data (optional)
- [ ] Unit tests pass (`pytest`)

---

## 🔍 Common Issues & Solutions

### Issue: ModuleNotFoundError
```bash
# Solution: Install dependencies
pip install -r requirements.txt
```

### Issue: MongoDB Connection Failed
```bash
# Solution: Check .env file
cat .env | grep MONGODB_URL
# Verify URL format and credentials
```

### Issue: Firebase Credentials Not Found
```bash
# Solution: Check file exists and path is correct
ls -la firebase-credentials.json
# Update .env with correct path
```

### Issue: Port 8000 Already in Use
```bash
# Solution: Use different port
uvicorn main:app --reload --port 8080
```

### Issue: CORS Errors
```bash
# Solution: Add frontend URL to ALLOWED_ORIGINS in .env
ALLOWED_ORIGINS=["http://localhost:3000","http://localhost:3001"]
```

---

## 🚀 Next Steps After Testing

1. **Frontend Integration:**
   - Configure Firebase in Next.js frontend
   - Set up API client with axios
   - Implement authentication pages

2. **Stripe Configuration:**
   - Add Stripe API keys to `.env`
   - Test payment endpoints
   - Set up webhook handlers

3. **Deployment:**
   - Set up production MongoDB
   - Configure environment variables
   - Deploy to cloud platform (Vercel, Railway, etc.)

---

## 📚 Additional Resources

- [Backend Structure Guide](STRUCTURE.md)
- [Firebase Setup Guide](FIREBASE_SETUP.md)
- [Main Setup Guide](SETUP_GUIDE.md)
- [API Documentation](http://localhost:8000/docs) (when server is running)
