"""
Order database model.
"""
from datetime import datetime
from typing import Optional, List
from bson import ObjectId
from pydantic import BaseModel, Field, ConfigDict
from app.models.owner_model import PyObjectId


class OrderItem(BaseModel):
    """Order item model."""
    product_id: str = Field(..., description="Product ID")
    product_name: str = Field(..., description="Product name")
    quantity: int = Field(..., gt=0, description="Quantity")
    price: float = Field(..., gt=0, description="Price per item")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "product_id": "product_id_123",
                "product_name": "Sample Product",
                "quantity": 2,
                "price": 29.99
            }
        }
    )


class OrderModel(BaseModel):
    """Order database model."""
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    owner_id: str = Field(..., description="Owner Firebase UID")
    customer_id: Optional[str] = Field(None, description="Customer Firebase UID (if logged in)")
    customer_email: str = Field(..., description="Customer email")
    customer_name: Optional[str] = Field(None, description="Customer name")
    items: List[OrderItem] = Field(..., description="Order items")
    total_amount: float = Field(..., gt=0, description="Total order amount")
    status: str = Field(default="pending", description="Order status: pending, confirmed, shipped, delivered, cancelled")
    shipping_address: Optional[str] = Field(None, description="Shipping address")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "owner_id": "firebase_uid_123",
                "customer_email": "customer@example.com",
                "items": [
                    {
                        "product_id": "product_id_123",
                        "product_name": "Sample Product",
                        "quantity": 2,
                        "price": 29.99
                    }
                ],
                "total_amount": 59.98,
                "status": "pending"
            }
        }
    )

