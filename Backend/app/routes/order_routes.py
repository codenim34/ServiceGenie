"""
Order routes for creating and managing orders.
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from app.routes.auth_routes import get_current_user, get_optional_user
from app.schemas.order_schema import OrderCreate, OrderUpdate, OrderResponse
from app.services.order_service import (
    create_order,
    get_order,
    get_orders_by_owner,
    get_orders_by_customer
)
from bson import ObjectId

router = APIRouter(prefix="/orders", tags=["orders"])


@router.post("", response_model=dict, status_code=201)
async def create_order_endpoint(
    order_data: OrderCreate,
    owner_id: str = Query(..., description="Owner Firebase UID"),
    current_user: Optional[dict] = Depends(get_optional_user)
):
    """
    Create a new order.
    
    Args:
        order_data: Order creation data
        owner_id: Owner Firebase UID (query parameter)
        current_user: Current authenticated user (optional)
        
    Returns:
        dict: Created order
    """
    customer_id = current_user["uid"] if current_user else None
    
    try:
        order = await create_order(owner_id, customer_id, order_data)
        return order
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("", response_model=List[dict])
async def get_orders(
    owner_id: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    current_user: Optional[dict] = Depends(get_optional_user)
):
    """
    Get orders (by owner or customer).
    
    Args:
        owner_id: Optional owner ID to filter orders
        skip: Number of orders to skip
        limit: Maximum number of orders to return
        current_user: Current authenticated user
        
    Returns:
        List[dict]: List of orders
    """
    if owner_id:
        # Get orders for a specific owner (requires auth for owner access)
        if not current_user:
            raise HTTPException(status_code=401, detail="Authentication required")
        orders = await get_orders_by_owner(owner_id, skip=skip, limit=limit)
    elif current_user:
        # Get orders for current customer
        orders = await get_orders_by_customer(current_user["uid"], skip=skip, limit=limit)
    else:
        raise HTTPException(status_code=401, detail="Authentication required")
    
    return orders


@router.get("/{order_id}", response_model=dict)
async def get_order_endpoint(order_id: str):
    """
    Get an order by ID.
    
    Args:
        order_id: Order ID
        
    Returns:
        dict: Order
    """
    if not ObjectId.is_valid(order_id):
        raise HTTPException(status_code=400, detail="Invalid order ID")
    
    order = await get_order(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

