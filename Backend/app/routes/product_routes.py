"""
Product routes for CRUD operations.
"""
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from typing import List, Optional
from app.routes.auth_routes import get_current_user
from app.schemas.product_schema import ProductCreate, ProductUpdate, ProductResponse
from app.services.product_service import (
    create_product,
    get_product,
    get_products_by_owner,
    get_all_products,
    update_product,
    delete_product
)
from app.utils.cloudinary_utils import upload_image_from_bytes
from bson import ObjectId

router = APIRouter(prefix="/products", tags=["products"])


@router.post("", response_model=dict, status_code=201)
async def create_product_endpoint(
    name: str = Form(...),
    sku: Optional[str] = Form(None),
    description: Optional[str] = Form(None),
    price: float = Form(...),
    category: str = Form(...),
    stock: int = Form(0),
    quantity: Optional[int] = Form(None),
    color: Optional[str] = Form(None),
    size: Optional[str] = Form(None),
    is_available: bool = Form(True),
    image: Optional[UploadFile] = File(None),
    current_user: dict = Depends(get_current_user)
):
    """
    Create a new product.
    
    Args:
        name: Product name
        description: Product description
        price: Product price
        category: Product category
        stock: Stock quantity
        is_available: Product availability
        image: Product image file
        current_user: Current authenticated user
        
    Returns:
        dict: Created product
    """
    owner_id = current_user["uid"]
    
    # Upload image if provided
    image_url = None
    if image:
        image_bytes = await image.read()
        image_url = await upload_image_from_bytes(image_bytes, image.filename or "product.jpg")
    
    resolved_stock = quantity if quantity is not None else stock

    product_data = ProductCreate(
        name=name,
        sku=sku,
        description=description,
        price=price,
        category=category,
        color=color,
        size=size,
        stock=resolved_stock,
        is_available=is_available,
        image_url=image_url
    )
    
    product = await create_product(owner_id, product_data)
    return product


@router.get("", response_model=List[dict])
async def get_products(
    owner_id: Optional[str] = None,
    category: Optional[str] = None,
    skip: int = 0,
    limit: int = 100
):
    """
    Get all products or products by owner.
    
    Args:
        owner_id: Optional owner ID to filter products
        category: Optional category filter
        skip: Number of products to skip
        limit: Maximum number of products to return
        
    Returns:
        List[dict]: List of products
    """
    if owner_id:
        products = await get_products_by_owner(owner_id, skip=skip, limit=limit)
    else:
        products = await get_all_products(skip=skip, limit=limit, category=category)
    return products


@router.get("/{product_id}", response_model=dict)
async def get_product_endpoint(product_id: str):
    """
    Get a product by ID.
    
    Args:
        product_id: Product ID
        
    Returns:
        dict: Product
    """
    if not ObjectId.is_valid(product_id):
        raise HTTPException(status_code=400, detail="Invalid product ID")
    
    product = await get_product(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.put("/{product_id}", response_model=dict)
async def update_product_endpoint(
    product_id: str,
    product_data: ProductUpdate,
    current_user: dict = Depends(get_current_user)
):
    """
    Update a product.
    
    Args:
        product_id: Product ID
        product_data: Product update data
        current_user: Current authenticated user
        
    Returns:
        dict: Updated product
    """
    if not ObjectId.is_valid(product_id):
        raise HTTPException(status_code=400, detail="Invalid product ID")
    
    owner_id = current_user["uid"]
    product = await update_product(product_id, owner_id, product_data)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found or access denied")
    return product


@router.delete("/{product_id}", status_code=204)
async def delete_product_endpoint(
    product_id: str,
    current_user: dict = Depends(get_current_user)
):
    """
    Delete a product.
    
    Args:
        product_id: Product ID
        current_user: Current authenticated user
    """
    if not ObjectId.is_valid(product_id):
        raise HTTPException(status_code=400, detail="Invalid product ID")
    
    owner_id = current_user["uid"]
    deleted = await delete_product(product_id, owner_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Product not found or access denied")

