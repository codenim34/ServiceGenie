from pydantic import BaseModel, Field
from typing import Optional, List, Dict
from datetime import datetime
from bson import ObjectId
from app.models.user import PyObjectId

class ProductBase(BaseModel):
    name: str
    description: str
    price: float = Field(gt=0)
    originalPrice: Optional[float] = None
    discount: Optional[float] = None
    category: str
    images: List[str] = []
    stock: int = Field(ge=0)
    rating: Optional[float] = Field(default=None, ge=0, le=5)
    reviews: Optional[int] = Field(default=0, ge=0)
    tags: List[str] = []
    specifications: Optional[Dict[str, str]] = {}
    featured: bool = False

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = Field(default=None, gt=0)
    originalPrice: Optional[float] = None
    discount: Optional[float] = None
    category: Optional[str] = None
    images: Optional[List[str]] = None
    stock: Optional[int] = Field(default=None, ge=0)
    rating: Optional[float] = Field(default=None, ge=0, le=5)
    reviews: Optional[int] = Field(default=None, ge=0)
    tags: Optional[List[str]] = None
    specifications: Optional[Dict[str, str]] = None
    featured: Optional[bool] = None

class ProductInDB(ProductBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    createdAt: datetime = Field(default_factory=datetime.utcnow)
    updatedAt: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        json_schema_extra = {
            "example": {
                "name": "Wireless Headphones",
                "description": "Premium noise-cancelling headphones",
                "price": 99.99,
                "originalPrice": 149.99,
                "category": "audio",
                "images": ["https://example.com/image.jpg"],
                "stock": 50,
                "rating": 4.5,
                "reviews": 120,
                "tags": ["wireless", "bluetooth", "audio"],
                "specifications": {
                    "battery": "30 hours",
                    "connectivity": "Bluetooth 5.0"
                }
            }
        }

class ProductResponse(BaseModel):
    id: str = Field(alias="_id")
    name: str
    description: str
    price: float
    originalPrice: Optional[float] = None
    discount: Optional[float] = None
    category: str
    images: List[str]
    stock: int
    rating: Optional[float] = None
    reviews: Optional[int] = None
    tags: List[str]
    specifications: Optional[Dict[str, str]] = None
    featured: bool = False
    createdAt: datetime
    updatedAt: datetime

    class Config:
        populate_by_name = True
