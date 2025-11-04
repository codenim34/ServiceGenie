from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app.models.user import UserCreate, UserResponse, UserUpdate, UserInDB
from app.core.database import get_database
from app.core.security import get_current_user
from datetime import datetime

router = APIRouter()

@router.post("/sync", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def sync_user(user_data: UserCreate):
    """
    Sync user from Firebase to MongoDB.
    Creates or updates user in database.
    """
    db = get_database()
    
    # Check if user exists
    existing_user = await db.users.find_one({"uid": user_data.uid})
    
    if existing_user:
        # Update user
        update_data = {
            "email": user_data.email,
            "displayName": user_data.displayName,
            "photoURL": user_data.photoURL,
            "updatedAt": datetime.utcnow()
        }
        await db.users.update_one(
            {"uid": user_data.uid},
            {"$set": update_data}
        )
        existing_user.update(update_data)
        return UserResponse(**existing_user)
    
    # Create new user
    user_dict = user_data.model_dump()
    user_dict["role"] = "customer"
    user_dict["createdAt"] = datetime.utcnow()
    user_dict["updatedAt"] = datetime.utcnow()
    
    result = await db.users.insert_one(user_dict)
    created_user = await db.users.find_one({"_id": result.inserted_id})
    
    return UserResponse(**created_user)

@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: UserInDB = Depends(get_current_user)):
    """
    Get current user information.
    """
    return UserResponse(**current_user.model_dump())

@router.put("/me", response_model=UserResponse)
async def update_current_user(
    user_update: UserUpdate,
    current_user: UserInDB = Depends(get_current_user)
):
    """
    Update current user information.
    """
    db = get_database()
    
    update_data = {k: v for k, v in user_update.model_dump().items() if v is not None}
    update_data["updatedAt"] = datetime.utcnow()
    
    await db.users.update_one(
        {"_id": current_user.id},
        {"$set": update_data}
    )
    
    updated_user = await db.users.find_one({"_id": current_user.id})
    return UserResponse(**updated_user)

@router.get("/{user_id}", response_model=UserResponse)
async def get_user_by_id(user_id: str):
    """
    Get user by ID (public information).
    """
    db = get_database()
    user = await db.users.find_one({"_id": user_id})
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return UserResponse(**user)
