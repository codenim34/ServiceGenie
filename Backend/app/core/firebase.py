"""
Firebase Admin SDK initialization and authentication utilities.
"""
import firebase_admin
from firebase_admin import credentials, auth
from pathlib import Path
from app.core.config import settings
from typing import Optional, Dict


# Global variable to track if Firebase is initialized
_firebase_app: Optional[firebase_admin.App] = None


def initialize_firebase():
    """
    Initialize Firebase Admin SDK.
    Returns the Firebase app instance.
    """
    global _firebase_app
    
    # Check if already initialized
    if _firebase_app is not None:
        return _firebase_app
    
    # Check if Firebase is already initialized by another module
    try:
        _firebase_app = firebase_admin.get_app()
        return _firebase_app
    except ValueError:
        # Not initialized yet, proceed with initialization
        pass
    
    # Get credentials file path
    creds_path = Path(settings.FIREBASE_CREDENTIAL_PATH)
    
    if not creds_path.exists():
        raise FileNotFoundError(
            f"Firebase credentials file not found at: {creds_path}\n"
            f"Please download it from Firebase Console and update FIREBASE_CREDENTIAL_PATH in .env"
        )
    
    # Initialize Firebase Admin SDK
    cred = credentials.Certificate(str(creds_path))
    _firebase_app = firebase_admin.initialize_app(cred)
    
    return _firebase_app


def verify_firebase_token(token: str) -> Dict:
    """
    Verify a Firebase ID token.
    
    Args:
        token: Firebase ID token from the client
        
    Returns:
        dict: Decoded token containing user information
        
    Raises:
        Exception: If the token is invalid or expired
    """
    # Ensure Firebase is initialized
    initialize_firebase()
    
    try:
        # Verify the token
        decoded_token = auth.verify_id_token(token)
        return decoded_token
    except Exception as e:
        raise Exception(f"Token verification failed: {str(e)}")


def get_user_by_uid(uid: str):
    """
    Get user information by UID.
    
    Args:
        uid: Firebase user UID
        
    Returns:
        UserRecord: Firebase user record
    """
    # Ensure Firebase is initialized
    initialize_firebase()
    
    try:
        user = auth.get_user(uid)
        return user
    except auth.UserNotFoundError:
        raise ValueError(f"User not found with UID: {uid}")
    except Exception as e:
        raise Exception(f"Error fetching user: {str(e)}")
