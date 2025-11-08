"""
Product database model.
"""
from datetime import datetime
from typing import Optional, List
from bson import ObjectId
from pydantic import BaseModel, Field, ConfigDict
from app.models.owner_model import PyObjectId


class ProductModel(BaseModel):
    """Product database model."""
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    owner_id: str = Field(..., description="Owner Firebase UID")
    name: str = Field(..., description="Product name")
    sku: Optional[str] = Field(None, description="Merchant defined product ID/SKU")
    description: Optional[str] = Field(None, description="Product description")
    price: float = Field(..., gt=0, description="Product price")
    category: str = Field(..., description="Product category")
    color: Optional[str] = Field(None, description="Primary color variant")
    size: Optional[str] = Field(None, description="Primary size variant")
    image_url: Optional[str] = Field(None, description="Product image URL from Cloudinary")
    stock: int = Field(default=0, ge=0, description="Stock quantity")
    is_available: bool = Field(default=True, description="Product availability")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "owner_id": "firebase_uid_123",
                "name": "Sample Product",
                "sku": "SKU-12345",
                "description": "A great product",
                "price": 29.99,
                "category": "Electronics",
                "color": "Blue",
                "size": "Medium",
                "image_url": "https://res.cloudinary.com/...",
                "stock": 100,
                "is_available": True
            }
        }
    )

