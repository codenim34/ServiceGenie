"""
Order service for business logic.
"""
from typing import List, Optional
from bson import ObjectId
from datetime import datetime
from app.core.db import get_database
from app.schemas.order_schema import OrderCreate, OrderUpdate
from app.services.product_service import get_product


async def create_order(owner_id: str, customer_id: Optional[str], order_data: OrderCreate) -> dict:
    """
    Create a new order.
    
    Args:
        owner_id: Owner Firebase UID
        customer_id: Customer Firebase UID (optional)
        order_data: Order creation data
        
    Returns:
        dict: Created order
    """
    db = get_database()
    orders_collection = db.orders
    products_collection = db.products
    
    # Calculate total and prepare items
    items = []
    total_amount = 0.0
    
    for item_create in order_data.items:
        product = await products_collection.find_one({"_id": ObjectId(item_create.product_id)})
        if not product or product.get("owner_id") != owner_id:
            raise ValueError(f"Product {item_create.product_id} not found or doesn't belong to this owner")
        
        if not product.get("is_available", False):
            raise ValueError(f"Product {item_create.product_id} is not available")
        
        if product.get("stock", 0) < item_create.quantity:
            raise ValueError(f"Insufficient stock for product {item_create.product_id}")
        
        item_price = product["price"]
        total_amount += item_price * item_create.quantity
        
        items.append({
            "product_id": item_create.product_id,
            "product_name": product["name"],
            "quantity": item_create.quantity,
            "price": item_price
        })
    
    # Create order
    order_dict = {
        "owner_id": owner_id,
        "customer_id": customer_id,
        "customer_email": order_data.customer_email,
        "customer_name": order_data.customer_name,
        "items": items,
        "total_amount": total_amount,
        "status": "pending",
        "shipping_address": order_data.shipping_address,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
    
    result = await orders_collection.insert_one(order_dict)
    order = await orders_collection.find_one({"_id": result.inserted_id})
    order["id"] = str(order["_id"])
    del order["_id"]
    return order


async def get_order(order_id: str) -> Optional[dict]:
    """
    Get an order by ID.
    
    Args:
        order_id: Order ID
        
    Returns:
        dict: Order or None if not found
    """
    db = get_database()
    orders_collection = db.orders
    
    order = await orders_collection.find_one({"_id": ObjectId(order_id)})
    if order:
        order["id"] = str(order["_id"])
        del order["_id"]
    return order


async def get_orders_by_owner(owner_id: str, skip: int = 0, limit: int = 100) -> List[dict]:
    """
    Get all orders for an owner.
    
    Args:
        owner_id: Owner Firebase UID
        skip: Number of orders to skip
        limit: Maximum number of orders to return
        
    Returns:
        List[dict]: List of orders
    """
    db = get_database()
    orders_collection = db.orders
    
    cursor = orders_collection.find({"owner_id": owner_id}).sort("created_at", -1).skip(skip).limit(limit)
    orders = await cursor.to_list(length=limit)
    
    for order in orders:
        order["id"] = str(order["_id"])
        del order["_id"]
    
    return orders


async def get_orders_by_customer(customer_id: str, skip: int = 0, limit: int = 100) -> List[dict]:
    """
    Get all orders for a customer.
    
    Args:
        customer_id: Customer Firebase UID
        skip: Number of orders to skip
        limit: Maximum number of orders to return
        
    Returns:
        List[dict]: List of orders
    """
    db = get_database()
    orders_collection = db.orders
    
    cursor = orders_collection.find({"customer_id": customer_id}).sort("created_at", -1).skip(skip).limit(limit)
    orders = await cursor.to_list(length=limit)
    
    for order in orders:
        order["id"] = str(order["_id"])
        del order["_id"]
    
    return orders


async def update_order_status(order_id: str, owner_id: str, order_data: OrderUpdate) -> Optional[dict]:
    """
    Update an order status.
    
    Args:
        order_id: Order ID
        owner_id: Owner Firebase UID
        order_data: Order update data
        
    Returns:
        dict: Updated order or None if not found
    """
    db = get_database()
    orders_collection = db.orders
    
    # Verify ownership
    order = await orders_collection.find_one({"_id": ObjectId(order_id), "owner_id": owner_id})
    if not order:
        return None
    
    update_data = {"updated_at": datetime.utcnow()}
    if order_data.status:
        update_data["status"] = order_data.status
    
    await orders_collection.update_one(
        {"_id": ObjectId(order_id)},
        {"$set": update_data}
    )
    
    updated_order = await orders_collection.find_one({"_id": ObjectId(order_id)})
    if updated_order:
        updated_order["id"] = str(updated_order["_id"])
        del updated_order["_id"]
    return updated_order


async def get_owner_analytics(owner_id: str) -> dict:
    """
    Get analytics for an owner (stub data for MVP).
    
    Args:
        owner_id: Owner Firebase UID
        
    Returns:
        dict: Analytics data
    """
    db = get_database()
    orders_collection = db.orders
    products_collection = db.products
    
    # Get total orders
    total_orders = await orders_collection.count_documents({"owner_id": owner_id})
    
    # Get total sales
    pipeline = [
        {"$match": {"owner_id": owner_id}},
        {"$group": {"_id": None, "total": {"$sum": "$total_amount"}}}
    ]
    sales_result = await orders_collection.aggregate(pipeline).to_list(length=1)
    total_sales = sales_result[0]["total"] if sales_result else 0.0
    
    # Get total products
    total_products = await products_collection.count_documents({"owner_id": owner_id})
    
    # Get pending orders
    pending_orders = await orders_collection.count_documents({"owner_id": owner_id, "status": "pending"})
    
    return {
        "total_orders": total_orders,
        "total_sales": total_sales,
        "total_products": total_products,
        "pending_orders": pending_orders
    }

