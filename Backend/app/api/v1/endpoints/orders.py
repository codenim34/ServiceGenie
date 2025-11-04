from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Optional
from app.models.order import OrderCreate, OrderResponse, OrderUpdate
from app.core.database import get_database
from app.core.security import get_current_user, get_current_admin_user
from app.models.user import UserInDB
from datetime import datetime
from bson import ObjectId

router = APIRouter()

@router.post("", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
async def create_order(
    order: OrderCreate,
    current_user: UserInDB = Depends(get_current_user)
):
    """
    Create a new order for the current user.
    """
    db = get_database()
    
    order_dict = order.model_dump()
    order_dict["userId"] = current_user.uid
    order_dict["status"] = "pending"
    order_dict["paymentStatus"] = "pending"
    order_dict["createdAt"] = datetime.utcnow()
    order_dict["updatedAt"] = datetime.utcnow()
    
    # Validate products and update stock
    for item in order.items:
        product = await db.products.find_one({"_id": ObjectId(item.productId)})
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Product {item.productId} not found"
            )
        if product["stock"] < item.quantity:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Insufficient stock for {product['name']}"
            )
    
    result = await db.orders.insert_one(order_dict)
    created_order = await db.orders.find_one({"_id": result.inserted_id})
    
    # Update product stock
    for item in order.items:
        await db.products.update_one(
            {"_id": ObjectId(item.productId)},
            {"$inc": {"stock": -item.quantity}}
        )
    
    return OrderResponse(**created_order)

@router.get("", response_model=List[OrderResponse])
async def get_orders(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    current_user: UserInDB = Depends(get_current_user)
):
    """
    Get all orders for the current user.
    """
    db = get_database()
    
    cursor = db.orders.find({"userId": current_user.uid}).skip(skip).limit(limit).sort("createdAt", -1)
    orders = await cursor.to_list(length=limit)
    
    return [OrderResponse(**order) for order in orders]

@router.get("/all", response_model=List[OrderResponse])
async def get_all_orders(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    status: Optional[str] = None,
    current_user: UserInDB = Depends(get_current_admin_user)
):
    """
    Get all orders (Admin only).
    """
    db = get_database()
    
    query = {}
    if status:
        query["status"] = status
    
    cursor = db.orders.find(query).skip(skip).limit(limit).sort("createdAt", -1)
    orders = await cursor.to_list(length=limit)
    
    return [OrderResponse(**order) for order in orders]

@router.get("/{order_id}", response_model=OrderResponse)
async def get_order(
    order_id: str,
    current_user: UserInDB = Depends(get_current_user)
):
    """
    Get a single order by ID.
    """
    db = get_database()
    
    if not ObjectId.is_valid(order_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid order ID"
        )
    
    order = await db.orders.find_one({"_id": ObjectId(order_id)})
    
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )
    
    # Check if user owns the order or is admin
    if order["userId"] != current_user.uid and current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view this order"
        )
    
    return OrderResponse(**order)

@router.put("/{order_id}", response_model=OrderResponse)
async def update_order(
    order_id: str,
    order_update: OrderUpdate,
    current_user: UserInDB = Depends(get_current_admin_user)
):
    """
    Update order status (Admin only).
    """
    db = get_database()
    
    if not ObjectId.is_valid(order_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid order ID"
        )
    
    existing_order = await db.orders.find_one({"_id": ObjectId(order_id)})
    if not existing_order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )
    
    update_data = {k: v for k, v in order_update.model_dump().items() if v is not None}
    update_data["updatedAt"] = datetime.utcnow()
    
    await db.orders.update_one(
        {"_id": ObjectId(order_id)},
        {"$set": update_data}
    )
    
    updated_order = await db.orders.find_one({"_id": ObjectId(order_id)})
    return OrderResponse(**updated_order)

@router.delete("/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
async def cancel_order(
    order_id: str,
    current_user: UserInDB = Depends(get_current_user)
):
    """
    Cancel an order.
    """
    db = get_database()
    
    if not ObjectId.is_valid(order_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid order ID"
        )
    
    order = await db.orders.find_one({"_id": ObjectId(order_id)})
    
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )
    
    # Check if user owns the order or is admin
    if order["userId"] != current_user.uid and current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to cancel this order"
        )
    
    if order["status"] in ["shipped", "delivered"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot cancel order that has been shipped or delivered"
        )
    
    # Update order status
    await db.orders.update_one(
        {"_id": ObjectId(order_id)},
        {"$set": {"status": "cancelled", "updatedAt": datetime.utcnow()}}
    )
    
    # Restore product stock
    for item in order["items"]:
        await db.products.update_one(
            {"_id": ObjectId(item["productId"])},
            {"$inc": {"stock": item["quantity"]}}
        )
    
    return None
