# Firebase Setup Guide

## 🔥 Setting Up Firebase for ServiceGenie

### Step 1: Create Firebase Project

1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Click "Add Project" or select existing project
3. Follow the setup wizard

### Step 2: Enable Authentication

1. In Firebase Console, go to **Authentication**
2. Click **Get Started**
3. Enable sign-in methods you want:
   - ✅ **Email/Password** (Recommended for MVP)
   - ✅ **Google** (Optional)
   - Other providers as needed

### Step 3: Generate Service Account Key

1. Go to **Project Settings** (gear icon)
2. Navigate to **Service Accounts** tab
3. Click **Generate New Private Key**
4. Click **Generate Key** - a JSON file will download
5. Save this file in your Backend directory (e.g., `Backend/firebase-credentials.json`)

### Step 4: Configure Environment Variable

Add to your `Backend/.env` file:

```env
# Firebase Configuration
FIREBASE_CREDENTIALS_PATH=firebase-credentials.json
```

Or use absolute path:
```env
FIREBASE_CREDENTIALS_PATH=E:\Projects\ServiceGenie\Backend\firebase-credentials.json
```

### Step 5: Secure the Credentials File

**Important:** Never commit credentials to Git!

Your `.gitignore` should already include:
```
# Firebase credentials
firebase-credentials.json
*-firebase-*.json
serviceAccountKey.json
```

### Step 6: Test Connection

Run the test script:
```bash
python tests/test_firebase_connection.py
```

## 📋 Firebase Credentials File Structure

Your downloaded JSON file should look like:

```json
{
  "type": "service_account",
  "project_id": "your-project-id",
  "private_key_id": "abc123...",
  "private_key": "-----BEGIN PRIVATE KEY-----\n...",
  "client_email": "firebase-adminsdk-xxxxx@your-project.iam.gserviceaccount.com",
  "client_id": "123456789",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/..."
}
```

## 🔒 Security Best Practices

1. **Never commit credentials to version control**
2. **Use environment variables** for file paths
3. **Restrict file permissions** (chmod 600 on Linux/Mac)
4. **Rotate keys periodically** (every 90 days recommended)
5. **Use different credentials** for dev/staging/production

## 🧪 Testing Firebase Features

### Test User Authentication
```bash
python tests/test_firebase_connection.py
```

### Test API Endpoints with Firebase Auth
```bash
# Run the server
uvicorn main:app --reload

# Test protected endpoint (you'll need a valid token)
curl -H "Authorization: Bearer YOUR_FIREBASE_TOKEN" \
     http://localhost:8000/api/v1/users/me
```

## 🌐 Frontend Integration

Once Firebase is working in backend, configure your Next.js frontend:

### Frontend `.env.local`:
```env
NEXT_PUBLIC_FIREBASE_API_KEY=your-api-key
NEXT_PUBLIC_FIREBASE_AUTH_DOMAIN=your-project.firebaseapp.com
NEXT_PUBLIC_FIREBASE_PROJECT_ID=your-project-id
NEXT_PUBLIC_FIREBASE_STORAGE_BUCKET=your-project.appspot.com
NEXT_PUBLIC_FIREBASE_MESSAGING_SENDER_ID=123456789
NEXT_PUBLIC_FIREBASE_APP_ID=1:123456789:web:abcdef
```

You can find these values in:
**Firebase Console → Project Settings → General → Your apps → SDK setup and configuration**

## ⚠️ Troubleshooting

### Error: "Credentials file not found"
- Check `FIREBASE_CREDENTIALS_PATH` in `.env`
- Verify the file exists at the specified path
- Use absolute path if relative path doesn't work

### Error: "Invalid credentials file"
- Ensure you downloaded the correct JSON file from Firebase
- Check the file isn't corrupted (should be valid JSON)
- Re-download the service account key if needed

### Error: "Permission denied"
- Check Firebase project is active (not deleted)
- Verify service account has proper permissions
- Ensure you're using the correct project

### Error: "Failed to initialize Firebase"
- Check internet connection
- Verify firewall isn't blocking Firebase API
- Try regenerating the service account key

## 📚 Additional Resources

- [Firebase Admin SDK Documentation](https://firebase.google.com/docs/admin/setup)
- [Firebase Authentication Documentation](https://firebase.google.com/docs/auth)
- [Service Account Permissions](https://firebase.google.com/docs/admin/setup#initialize_the_sdk_in_non-google_environments)

## ✅ Checklist

- [ ] Firebase project created
- [ ] Authentication enabled
- [ ] Service account key downloaded
- [ ] Credentials file saved in Backend directory
- [ ] `FIREBASE_CREDENTIALS_PATH` set in `.env`
- [ ] Credentials file added to `.gitignore`
- [ ] Connection test passed
- [ ] Frontend Firebase config ready (for later)
