from pydantic import BaseModel, Field
from typing import List, Literal, Optional
from datetime import datetime
from bson import ObjectId
from app.models.user import PyObjectId

class ShippingAddress(BaseModel):
    name: str
    phone: str
    address: str
    city: str
    postalCode: str
    country: str = "Bangladesh"

class OrderItem(BaseModel):
    productId: str
    name: str
    price: float
    quantity: int = Field(gt=0)
    image: str

class OrderBase(BaseModel):
    items: List[OrderItem]
    totalAmount: float = Field(gt=0)
    shippingAddress: ShippingAddress
    paymentMethod: str = "stripe"

class OrderCreate(OrderBase):
    pass

class OrderUpdate(BaseModel):
    status: Optional[Literal["pending", "processing", "shipped", "delivered", "cancelled"]] = None
    paymentStatus: Optional[Literal["pending", "paid", "failed"]] = None

class OrderInDB(OrderBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    userId: str
    status: Literal["pending", "processing", "shipped", "delivered", "cancelled"] = "pending"
    paymentStatus: Literal["pending", "paid", "failed"] = "pending"
    createdAt: datetime = Field(default_factory=datetime.utcnow)
    updatedAt: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        json_schema_extra = {
            "example": {
                "userId": "user-123",
                "items": [
                    {
                        "productId": "prod-123",
                        "name": "Product Name",
                        "price": 99.99,
                        "quantity": 2,
                        "image": "https://example.com/image.jpg"
                    }
                ],
                "totalAmount": 199.98,
                "status": "pending",
                "paymentStatus": "pending",
                "paymentMethod": "stripe",
                "shippingAddress": {
                    "name": "John Doe",
                    "phone": "+880123456789",
                    "address": "123 Main St",
                    "city": "Dhaka",
                    "postalCode": "1000",
                    "country": "Bangladesh"
                }
            }
        }

class OrderResponse(BaseModel):
    id: str = Field(alias="_id")
    userId: str
    items: List[OrderItem]
    totalAmount: float
    status: str
    paymentStatus: str
    paymentMethod: str
    shippingAddress: ShippingAddress
    createdAt: datetime
    updatedAt: datetime

    class Config:
        populate_by_name = True
