"""
Order Pydantic schemas for request/response validation.
"""
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, EmailStr


class OrderItemCreate(BaseModel):
    """Schema for creating an order item."""
    product_id: str
    quantity: int = Field(..., gt=0)


class OrderItemResponse(BaseModel):
    """Schema for order item response."""
    product_id: str
    product_name: str
    quantity: int
    price: float


class OrderCreate(BaseModel):
    """Schema for creating an order."""
    customer_email: EmailStr
    customer_name: Optional[str] = None
    items: List[OrderItemCreate]
    shipping_address: Optional[str] = None


class OrderUpdate(BaseModel):
    """Schema for updating an order."""
    status: Optional[str] = Field(None, pattern="^(pending|confirmed|shipped|delivered|cancelled)$")


class OrderResponse(BaseModel):
    """Schema for order response."""
    id: str
    owner_id: str
    customer_id: Optional[str] = None
    customer_email: str
    customer_name: Optional[str] = None
    items: List[OrderItemResponse]
    total_amount: float
    status: str
    shipping_address: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

