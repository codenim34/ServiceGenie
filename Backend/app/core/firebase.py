"""
Firebase Admin SDK initialization and authentication utilities.
"""
import firebase_admin
from firebase_admin import credentials, auth
from pathlib import Path
from .config import settings


# Global variable to track if Firebase is initialized
_firebase_app = None


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
    creds_path = Path(settings.FIREBASE_CREDENTIALS_PATH)
    
    if not creds_path.exists():
        raise FileNotFoundError(
            f"Firebase credentials file not found at: {creds_path}\n"
            f"Please download it from Firebase Console and update FIREBASE_CREDENTIALS_PATH in .env"
        )
    
    # Initialize Firebase Admin SDK
    cred = credentials.Certificate(str(creds_path))
    _firebase_app = firebase_admin.initialize_app(cred)
    
    return _firebase_app


def verify_firebase_token(token: str) -> dict:
    """
    Verify a Firebase ID token.
    
    Args:
        token: Firebase ID token from the client
        
    Returns:
        dict: Decoded token containing user information
        
    Raises:
        auth.InvalidIdTokenError: If the token is invalid
        auth.ExpiredIdTokenError: If the token has expired
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


def create_custom_token(uid: str, additional_claims: dict = None) -> bytes:
    """
    Create a custom token for a user.
    
    Args:
        uid: Firebase user UID
        additional_claims: Optional additional claims to include in the token
        
    Returns:
        bytes: Custom token
    """
    # Ensure Firebase is initialized
    initialize_firebase()
    
    try:
        custom_token = auth.create_custom_token(uid, additional_claims)
        return custom_token
    except Exception as e:
        raise Exception(f"Error creating custom token: {str(e)}")


def delete_user(uid: str):
    """
    Delete a user by UID.
    
    Args:
        uid: Firebase user UID
    """
    # Ensure Firebase is initialized
    initialize_firebase()
    
    try:
        auth.delete_user(uid)
    except auth.UserNotFoundError:
        raise ValueError(f"User not found with UID: {uid}")
    except Exception as e:
        raise Exception(f"Error deleting user: {str(e)}")


def list_users(max_results: int = 1000):
    """
    List all users.
    
    Args:
        max_results: Maximum number of users to return
        
    Returns:
        ListUsersPage: Page of users
    """
    # Ensure Firebase is initialized
    initialize_firebase()
    
    try:
        page = auth.list_users(max_results=max_results)
        return page
    except Exception as e:
        raise Exception(f"Error listing users: {str(e)}")


# Initialize Firebase when module is imported
try:
    initialize_firebase()
except Exception as e:
    print(f"Warning: Firebase initialization failed: {e}")
    print("Firebase will be initialized on first use.")