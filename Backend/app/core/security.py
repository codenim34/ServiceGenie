from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthCredential
from app.core.firebase import verify_firebase_token
from app.core.database import get_database
from app.models.user import UserInDB

security = HTTPBearer()

async def get_current_user(
    credentials: HTTPAuthCredential = Depends(security)
) -> UserInDB:
    """
    Dependency to get the current authenticated user from Firebase token.
    """
    token = credentials.credentials
    
    # Verify Firebase token
    firebase_user = await verify_firebase_token(token)
    
    # Get user from database
    db = get_database()
    user_dict = await db.users.find_one({"uid": firebase_user["uid"]})
    
    if not user_dict:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return UserInDB(**user_dict)

async def get_current_active_user(
    current_user: UserInDB = Depends(get_current_user)
) -> UserInDB:
    """
    Dependency to get the current active user.
    """
    return current_user

async def get_current_admin_user(
    current_user: UserInDB = Depends(get_current_user)
) -> UserInDB:
    """
    Dependency to verify admin user.
    """
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    return current_user
