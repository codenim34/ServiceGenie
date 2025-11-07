"""
Product service for business logic.
"""
from typing import List, Optional
from bson import ObjectId
from app.core.db import get_database
from app.models.product_model import ProductModel
from app.schemas.product_schema import ProductCreate, ProductUpdate


async def create_product(owner_id: str, product_data: ProductCreate) -> dict:
    """
    Create a new product.
    
    Args:
        owner_id: Owner Firebase UID
        product_data: Product creation data
        
    Returns:
        dict: Created product
    """
    db = get_database()
    products_collection = db.products
    
    product_dict = product_data.model_dump()
    product_dict["owner_id"] = owner_id
    
    result = await products_collection.insert_one(product_dict)
    product = await products_collection.find_one({"_id": result.inserted_id})
    product["id"] = str(product["_id"])
    del product["_id"]
    return product


async def get_product(product_id: str) -> Optional[dict]:
    """
    Get a product by ID.
    
    Args:
        product_id: Product ID
        
    Returns:
        dict: Product or None if not found
    """
    db = get_database()
    products_collection = db.products
    
    product = await products_collection.find_one({"_id": ObjectId(product_id)})
    if product:
        product["id"] = str(product["_id"])
        del product["_id"]
    return product


async def get_products_by_owner(owner_id: str, skip: int = 0, limit: int = 100) -> List[dict]:
    """
    Get all products for an owner.
    
    Args:
        owner_id: Owner Firebase UID
        skip: Number of products to skip
        limit: Maximum number of products to return
        
    Returns:
        List[dict]: List of products
    """
    db = get_database()
    products_collection = db.products
    
    cursor = products_collection.find({"owner_id": owner_id}).skip(skip).limit(limit)
    products = await cursor.to_list(length=limit)
    
    for product in products:
        product["id"] = str(product["_id"])
        del product["_id"]
    
    return products


async def get_all_products(skip: int = 0, limit: int = 100, category: Optional[str] = None) -> List[dict]:
    """
    Get all products (for customer browsing).
    
    Args:
        skip: Number of products to skip
        limit: Maximum number of products to return
        category: Optional category filter
        
    Returns:
        List[dict]: List of products
    """
    db = get_database()
    products_collection = db.products
    
    query = {"is_available": True}
    if category:
        query["category"] = category
    
    cursor = products_collection.find(query).skip(skip).limit(limit)
    products = await cursor.to_list(length=limit)
    
    for product in products:
        product["id"] = str(product["_id"])
        del product["_id"]
    
    return products


async def update_product(product_id: str, owner_id: str, product_data: ProductUpdate) -> Optional[dict]:
    """
    Update a product.
    
    Args:
        product_id: Product ID
        owner_id: Owner Firebase UID
        product_data: Product update data
        
    Returns:
        dict: Updated product or None if not found
    """
    db = get_database()
    products_collection = db.products
    
    # Verify ownership
    product = await products_collection.find_one({"_id": ObjectId(product_id), "owner_id": owner_id})
    if not product:
        return None
    
    update_data = product_data.model_dump(exclude_unset=True)
    update_data["updated_at"] = product_data.model_dump().get("updated_at")
    
    await products_collection.update_one(
        {"_id": ObjectId(product_id)},
        {"$set": update_data}
    )
    
    updated_product = await products_collection.find_one({"_id": ObjectId(product_id)})
    if updated_product:
        updated_product["id"] = str(updated_product["_id"])
        del updated_product["_id"]
    return updated_product


async def delete_product(product_id: str, owner_id: str) -> bool:
    """
    Delete a product.
    
    Args:
        product_id: Product ID
        owner_id: Owner Firebase UID
        
    Returns:
        bool: True if deleted, False if not found
    """
    db = get_database()
    products_collection = db.products
    
    result = await products_collection.delete_one({"_id": ObjectId(product_id), "owner_id": owner_id})
    return result.deleted_count > 0

