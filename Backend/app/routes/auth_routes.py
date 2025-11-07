"""
Authentication routes for Firebase token verification.
"""
from fastapi import APIRouter, Depends, HTTPException, Header
from typing import Optional
from app.core.firebase import verify_firebase_token, get_user_by_uid
from pydantic import BaseModel

router = APIRouter(prefix="/auth", tags=["auth"])


class TokenVerifyRequest(BaseModel):
    """Token verification request."""
    token: str


class TokenVerifyResponse(BaseModel):
    """Token verification response."""
    valid: bool
    uid: Optional[str] = None
    email: Optional[str] = None
    message: Optional[str] = None


def get_current_user(authorization: Optional[str] = Header(None)) -> dict:
    """
    Dependency to get current user from Firebase token.
    
    Args:
        authorization: Authorization header with Bearer token
        
    Returns:
        dict: Decoded Firebase token
        
    Raises:
        HTTPException: If token is invalid or missing
    """
    if not authorization:
        raise HTTPException(status_code=401, detail="Authorization header missing")
    
    try:
        # Extract token from "Bearer <token>"
        token = authorization.replace("Bearer ", "")
        decoded_token = verify_firebase_token(token)
        return decoded_token
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Invalid token: {str(e)}")


def get_optional_user(authorization: Optional[str] = Header(None)) -> Optional[dict]:
    """
    Optional dependency to get current user from Firebase token.
    Returns None if no token is provided.
    
    Args:
        authorization: Authorization header with Bearer token
        
    Returns:
        dict: Decoded Firebase token or None
    """
    if not authorization:
        return None
    
    try:
        token = authorization.replace("Bearer ", "")
        decoded_token = verify_firebase_token(token)
        return decoded_token
    except Exception:
        return None


@router.post("/verify", response_model=TokenVerifyResponse)
async def verify_token(request: TokenVerifyRequest):
    """
    Verify a Firebase ID token.
    
    Args:
        request: Token verification request
        
    Returns:
        TokenVerifyResponse: Verification result
    """
    try:
        decoded_token = verify_firebase_token(request.token)
        return TokenVerifyResponse(
            valid=True,
            uid=decoded_token.get("uid"),
            email=decoded_token.get("email"),
            message="Token is valid"
        )
    except Exception as e:
        return TokenVerifyResponse(
            valid=False,
            message=f"Token verification failed: {str(e)}"
        )


@router.get("/user/{uid}")
async def get_user(uid: str):
    """
    Get user information by UID.
    
    Args:
        uid: Firebase user UID
        
    Returns:
        dict: User information
    """
    try:
        user = get_user_by_uid(uid)
        return {
            "uid": user.uid,
            "email": user.email,
            "display_name": user.display_name,
            "photo_url": user.photo_url
        }
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

