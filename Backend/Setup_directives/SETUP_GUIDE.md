# Backend Environment Setup & Database Connection Test

## 📋 Environment File Configuration

### ✅ Your Setup is Correct!

**Backend**: `.env` file (Python/FastAPI)
**Frontend**: `.env.local` file (Next.js)

This is the proper way to separate configurations!

## 🔧 Backend Setup Steps

### 1. Create Virtual Environment (if not done)

```bash
cd Backend
python -m venv venv
```

### 2. Activate Virtual Environment

**Windows (PowerShell/CMD):**
```bash
venv\Scripts\activate
```

**Windows (Git Bash):**
```bash
source venv/Scripts/activate
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Test MongoDB Connection

```bash
python scripts/test_db_connection.py
```

This will:
- ✅ Test connection to your MongoDB Atlas cluster
- ✅ Verify read/write operations
- ✅ Show existing collections and document counts
- ✅ Display database statistics

### 5. Seed Database (Optional)

```bash
python scripts/seed_db.py
```

This adds:
- 6 Categories (Electronics, Fashion, Watches, etc.)
- 8 Sample Products with images

### 6. Start the Backend Server

```bash
uvicorn main:app --reload
```

Access at:
- API: http://localhost:8000
- Docs: http://localhost:8000/docs

## 🔐 Your MongoDB Configuration

```env
MONGODB_URL=mongodb+srv://tasnimashraf*******@cluster0.lytnrtd.mongodb.net/?appName=Cluster0
DATABASE_NAME=servicegenie
```

✅ **Password encoding looks correct!** (`@` = %40, `#` = %23)

## ⚠️ MongoDB Atlas Checklist

Make sure in your MongoDB Atlas dashboard:

1. **Cluster is Running** ✓
2. **Network Access**: Your IP address is whitelisted
   - Go to: Network Access → Add IP Address → Allow Access from Anywhere (0.0.0.0/0)
3. **Database User**: Username `tasnimashraf` exists with correct password
4. **Database Access**: User has read/write permissions

## 🧪 Quick Test Commands

```bash
# Full workflow
cd Backend
source venv/Scripts/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
python scripts/test_db_connection.py
python scripts/seed_db.py
uvicorn main:app --reload
```

## 🎯 Expected Test Output

If successful, you'll see:
```
============================================================
🔍 ServiceGenie - MongoDB Connection Test
============================================================

📡 Connecting to: ...@cluster0.lytnrtd.mongodb.net/...
📊 Database name: servicegenie

⏳ Testing connection...
✅ Connection successful! MongoDB is responding.

📂 Existing collections:
   (No collections yet - database is empty)

✍️  Testing write operation...
✅ Write successful! Document ID: ...

📖 Testing read operation...
✅ Read successful! Retrieved: ServiceGenie Connection Test

🧹 Cleaning up test document...
✅ Cleanup successful!

📊 Database Statistics:
   - Collections: 0
   - Data Size: 0 bytes
   - Storage Size: 0 bytes

============================================================
🎉 All tests passed! Your MongoDB connection is working perfectly!
============================================================
```

## 🐛 Common Issues & Solutions

### Issue 1: Module Not Found
```
ModuleNotFoundError: No module named 'motor'
```
**Solution**: Install dependencies
```bash
pip install -r requirements.txt
```

### Issue 2: Connection Timeout
```
ServerSelectionTimeoutError
```
**Solutions**:
- Check MongoDB Atlas cluster is running
- Whitelist your IP in Network Access
- Verify internet connection

### Issue 3: Authentication Failed
```
Authentication failed
```
**Solutions**:
- Verify username and password
- Check special characters are URL-encoded:
  - `@` → `%40`
  - `#` → `%23`
  - `$` → `%24`

### Issue 4: Import Error
```
cannot import name 'settings' from 'app.core.config'
```
**Solution**: Make sure you're in Backend directory and venv is activated

## 📝 Next Steps After Successful Connection

1. ✅ Connection test passes
2. 🌱 Seed database with sample data
3. 🚀 Start FastAPI server
4. 📖 Test endpoints at http://localhost:8000/docs
5. 🎨 Start frontend development

## 🔗 Frontend Environment

Create `Frontend/.env.local`:
```env
NEXT_PUBLIC_API_URL=http://localhost:8000/api

# Firebase Config (get from Firebase Console)
NEXT_PUBLIC_FIREBASE_API_KEY=your_api_key
NEXT_PUBLIC_FIREBASE_AUTH_DOMAIN=your_project.firebaseapp.com
NEXT_PUBLIC_FIREBASE_PROJECT_ID=your_project_id
NEXT_PUBLIC_FIREBASE_STORAGE_BUCKET=your_project.appspot.com
NEXT_PUBLIC_FIREBASE_MESSAGING_SENDER_ID=your_sender_id
NEXT_PUBLIC_FIREBASE_APP_ID=your_app_id

# Stripe Config
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=pk_test_your_key
```

---

**Ready to test?** Run the commands above and let me know the result! 🚀
