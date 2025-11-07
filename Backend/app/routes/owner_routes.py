"""
Owner routes for owner management and analytics.
"""
from fastapi import APIRouter, Depends, HTTPException
from typing import Optional
from app.routes.auth_routes import get_current_user
from app.core.db import get_database
from app.schemas.owner_schema import OwnerCreate, OwnerUpdate, OwnerResponse
from app.services.order_service import get_owner_analytics
from datetime import datetime

router = APIRouter(prefix="/owners", tags=["owners"])


@router.post("", response_model=dict, status_code=201)
async def create_owner(
    owner_data: OwnerCreate,
    current_user: dict = Depends(get_current_user)
):
    """
    Create or update owner profile.
    
    Args:
        owner_data: Owner creation data
        current_user: Current authenticated user
        
    Returns:
        dict: Created/updated owner
    """
    db = get_database()
    owners_collection = db.owners
    
    # Check if owner already exists
    existing_owner = await owners_collection.find_one({"firebase_uid": current_user["uid"]})
    
    owner_dict = owner_data.model_dump()
    owner_dict["firebase_uid"] = current_user["uid"]
    owner_dict["email"] = current_user.get("email", owner_data.email)
    owner_dict["updated_at"] = datetime.utcnow()
    
    if existing_owner:
        # Update existing owner
        await owners_collection.update_one(
            {"firebase_uid": current_user["uid"]},
            {"$set": owner_dict}
        )
        owner = await owners_collection.find_one({"firebase_uid": current_user["uid"]})
    else:
        # Create new owner
        owner_dict["created_at"] = datetime.utcnow()
        result = await owners_collection.insert_one(owner_dict)
        owner = await owners_collection.find_one({"_id": result.inserted_id})
    
    owner["id"] = str(owner["_id"])
    del owner["_id"]
    return owner


@router.get("/me", response_model=dict)
async def get_owner_profile(current_user: dict = Depends(get_current_user)):
    """
    Get current owner profile.
    
    Args:
        current_user: Current authenticated user
        
    Returns:
        dict: Owner profile
    """
    db = get_database()
    owners_collection = db.owners
    
    owner = await owners_collection.find_one({"firebase_uid": current_user["uid"]})
    if not owner:
        raise HTTPException(status_code=404, detail="Owner profile not found")
    
    owner["id"] = str(owner["_id"])
    del owner["_id"]
    return owner


@router.put("/me", response_model=dict)
async def update_owner_profile(
    owner_data: OwnerUpdate,
    current_user: dict = Depends(get_current_user)
):
    """
    Update current owner profile.
    
    Args:
        owner_data: Owner update data
        current_user: Current authenticated user
        
    Returns:
        dict: Updated owner profile
    """
    db = get_database()
    owners_collection = db.owners
    
    update_data = owner_data.model_dump(exclude_unset=True)
    update_data["updated_at"] = datetime.utcnow()
    
    result = await owners_collection.update_one(
        {"firebase_uid": current_user["uid"]},
        {"$set": update_data}
    )
    
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Owner profile not found")
    
    owner = await owners_collection.find_one({"firebase_uid": current_user["uid"]})
    owner["id"] = str(owner["_id"])
    del owner["_id"]
    return owner


@router.get("/me/analytics", response_model=dict)
async def get_analytics(current_user: dict = Depends(get_current_user)):
    """
    Get owner analytics.
    
    Args:
        current_user: Current authenticated user
        
    Returns:
        dict: Analytics data
    """
    owner_id = current_user["uid"]
    analytics = await get_owner_analytics(owner_id)
    return analytics

