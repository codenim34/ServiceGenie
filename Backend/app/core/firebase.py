import firebase_admin
from firebase_admin import credentials, auth
from app.core.config import settings
from fastapi import HTTPException, status

# Initialize Firebase Admin SDK
try:
    cred = credentials.Certificate(settings.FIREBASE_CREDENTIALS_PATH)
    firebase_admin.initialize_app(cred)
    print("✅ Firebase Admin SDK initialized")
except Exception as e:
    print(f"⚠️ Firebase initialization error: {e}")

async def verify_firebase_token(token: str) -> dict:
    """
    Verify Firebase ID token and return user data.
    """
    try:
        decoded_token = auth.verify_id_token(token)
        return decoded_token
    except auth.InvalidIdTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token"
        )
    except auth.ExpiredIdTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication token has expired"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Authentication error: {str(e)}"
        )
