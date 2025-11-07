"""
Product Pydantic schemas for request/response validation.
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class ProductBase(BaseModel):
    """Base product schema."""
    name: str
    description: Optional[str] = None
    price: float = Field(..., gt=0)
    category: str
    stock: int = Field(default=0, ge=0)
    is_available: bool = Field(default=True)


class ProductCreate(ProductBase):
    """Schema for creating a product."""
    image_url: Optional[str] = None


class ProductUpdate(BaseModel):
    """Schema for updating a product."""
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = Field(None, gt=0)
    category: Optional[str] = None
    image_url: Optional[str] = None
    stock: Optional[int] = Field(None, ge=0)
    is_available: Optional[bool] = None


class ProductResponse(ProductBase):
    """Schema for product response."""
    id: str
    owner_id: str
    image_url: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

