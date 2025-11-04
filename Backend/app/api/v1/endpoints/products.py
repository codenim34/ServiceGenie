from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Optional
from app.models.product import ProductCreate, ProductResponse, ProductUpdate, ProductInDB
from app.core.database import get_database
from app.core.security import get_current_admin_user, get_current_user
from datetime import datetime
from bson import ObjectId

router = APIRouter()

@router.get("", response_model=dict)
async def get_products(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    category: Optional[str] = None,
    search: Optional[str] = None,
    featured: Optional[bool] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
):
    """
    Get all products with filters and pagination.
    """
    db = get_database()
    
    # Build query
    query = {}
    if category:
        query["category"] = category
    if featured is not None:
        query["featured"] = featured
    if search:
        query["$or"] = [
            {"name": {"$regex": search, "$options": "i"}},
            {"description": {"$regex": search, "$options": "i"}},
            {"tags": {"$in": [search]}}
        ]
    if min_price is not None or max_price is not None:
        query["price"] = {}
        if min_price is not None:
            query["price"]["$gte"] = min_price
        if max_price is not None:
            query["price"]["$lte"] = max_price
    
    # Get total count
    total = await db.products.count_documents(query)
    
    # Get products
    cursor = db.products.find(query).skip(skip).limit(limit).sort("createdAt", -1)
    products = await cursor.to_list(length=limit)
    
    return {
        "products": [ProductResponse(**product) for product in products],
        "total": total,
        "skip": skip,
        "limit": limit
    }

@router.get("/{product_id}", response_model=ProductResponse)
async def get_product(product_id: str):
    """
    Get a single product by ID.
    """
    db = get_database()
    
    if not ObjectId.is_valid(product_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid product ID"
        )
    
    product = await db.products.find_one({"_id": ObjectId(product_id)})
    
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    
    return ProductResponse(**product)

@router.post("", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
async def create_product(
    product: ProductCreate,
    current_user = Depends(get_current_admin_user)
):
    """
    Create a new product (Admin only).
    """
    db = get_database()
    
    product_dict = product.model_dump()
    product_dict["createdAt"] = datetime.utcnow()
    product_dict["updatedAt"] = datetime.utcnow()
    
    # Calculate discount if originalPrice is provided
    if product.originalPrice and product.price < product.originalPrice:
        product_dict["discount"] = round(
            ((product.originalPrice - product.price) / product.originalPrice) * 100, 2
        )
    
    result = await db.products.insert_one(product_dict)
    created_product = await db.products.find_one({"_id": result.inserted_id})
    
    return ProductResponse(**created_product)

@router.put("/{product_id}", response_model=ProductResponse)
async def update_product(
    product_id: str,
    product_update: ProductUpdate,
    current_user = Depends(get_current_admin_user)
):
    """
    Update a product (Admin only).
    """
    db = get_database()
    
    if not ObjectId.is_valid(product_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid product ID"
        )
    
    # Check if product exists
    existing_product = await db.products.find_one({"_id": ObjectId(product_id)})
    if not existing_product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    
    update_data = {k: v for k, v in product_update.model_dump().items() if v is not None}
    update_data["updatedAt"] = datetime.utcnow()
    
    # Recalculate discount if prices are updated
    if "price" in update_data or "originalPrice" in update_data:
        price = update_data.get("price", existing_product.get("price"))
        original_price = update_data.get("originalPrice", existing_product.get("originalPrice"))
        
        if original_price and price < original_price:
            update_data["discount"] = round(
                ((original_price - price) / original_price) * 100, 2
            )
    
    await db.products.update_one(
        {"_id": ObjectId(product_id)},
        {"$set": update_data}
    )
    
    updated_product = await db.products.find_one({"_id": ObjectId(product_id)})
    return ProductResponse(**updated_product)

@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(
    product_id: str,
    current_user = Depends(get_current_admin_user)
):
    """
    Delete a product (Admin only).
    """
    db = get_database()
    
    if not ObjectId.is_valid(product_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid product ID"
        )
    
    result = await db.products.delete_one({"_id": ObjectId(product_id)})
    
    if result.deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    
    return None
