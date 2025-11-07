"""
Owner database model.
"""
from datetime import datetime
from typing import Optional
from bson import ObjectId
from pydantic import BaseModel, Field, ConfigDict


class PyObjectId(ObjectId):
    """Custom ObjectId type for Pydantic."""
    @classmethod
    def __get_validators__(cls):
        yield cls.validate
    
    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)
    
    @classmethod
    def __get_pydantic_json_schema__(cls, field_schema):
        field_schema.update(type="string")


class OwnerModel(BaseModel):
    """Owner database model."""
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    firebase_uid: str = Field(..., description="Firebase user UID")
    email: str = Field(..., description="Owner email")
    business_name: Optional[str] = Field(None, description="Business name")
    phone: Optional[str] = Field(None, description="Phone number")
    address: Optional[str] = Field(None, description="Business address")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "firebase_uid": "firebase_uid_123",
                "email": "owner@example.com",
                "business_name": "My Shop",
                "phone": "+1234567890",
                "address": "123 Main St"
            }
        }
    )

