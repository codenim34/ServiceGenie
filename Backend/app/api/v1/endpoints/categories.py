from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app.models.category import CategoryCreate, CategoryResponse, CategoryUpdate
from app.core.database import get_database
from app.core.security import get_current_admin_user
from datetime import datetime
from bson import ObjectId

router = APIRouter()

@router.get("", response_model=List[CategoryResponse])
async def get_categories():
    """
    Get all categories.
    """
    db = get_database()
    cursor = db.categories.find({})
    categories = await cursor.to_list(length=100)
    
    return [CategoryResponse(**category) for category in categories]

@router.get("/{category_id}", response_model=CategoryResponse)
async def get_category(category_id: str):
    """
    Get a single category by ID.
    """
    db = get_database()
    
    if not ObjectId.is_valid(category_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid category ID"
        )
    
    category = await db.categories.find_one({"_id": ObjectId(category_id)})
    
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )
    
    return CategoryResponse(**category)

@router.post("", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
async def create_category(
    category: CategoryCreate,
    current_user = Depends(get_current_admin_user)
):
    """
    Create a new category (Admin only).
    """
    db = get_database()
    
    # Check if slug already exists
    existing = await db.categories.find_one({"slug": category.slug})
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Category with this slug already exists"
        )
    
    category_dict = category.model_dump()
    category_dict["createdAt"] = datetime.utcnow()
    category_dict["updatedAt"] = datetime.utcnow()
    
    result = await db.categories.insert_one(category_dict)
    created_category = await db.categories.find_one({"_id": result.inserted_id})
    
    return CategoryResponse(**created_category)

@router.put("/{category_id}", response_model=CategoryResponse)
async def update_category(
    category_id: str,
    category_update: CategoryUpdate,
    current_user = Depends(get_current_admin_user)
):
    """
    Update a category (Admin only).
    """
    db = get_database()
    
    if not ObjectId.is_valid(category_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid category ID"
        )
    
    existing_category = await db.categories.find_one({"_id": ObjectId(category_id)})
    if not existing_category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )
    
    update_data = {k: v for k, v in category_update.model_dump().items() if v is not None}
    update_data["updatedAt"] = datetime.utcnow()
    
    await db.categories.update_one(
        {"_id": ObjectId(category_id)},
        {"$set": update_data}
    )
    
    updated_category = await db.categories.find_one({"_id": ObjectId(category_id)})
    return CategoryResponse(**updated_category)

@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(
    category_id: str,
    current_user = Depends(get_current_admin_user)
):
    """
    Delete a category (Admin only).
    """
    db = get_database()
    
    if not ObjectId.is_valid(category_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid category ID"
        )
    
    result = await db.categories.delete_one({"_id": ObjectId(category_id)})
    
    if result.deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )
    
    return None
