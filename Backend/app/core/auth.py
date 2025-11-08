"""
Simple authentication service for prototype
"""
from datetime import datetime, timedelta
from typing import Optional
import jwt
from app.core.memory_db import db

# This should be changed in production
SECRET_KEY = "prototype-secret-key-change-in-production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str) -> Optional[dict]:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.JWTError:
        return None

def authenticate_user(email: str, password: str) -> Optional[dict]:
    user = db.get_user_by_email(email)
    if user and user["password"] == password:  # In production, use proper password hashing
        return user
    return None

def get_current_user(token: str) -> Optional[dict]:
    payload = verify_token(token)
    if payload:
        user_id = payload.get("sub")
        if user_id:
            return db.get_user(user_id)
    return None