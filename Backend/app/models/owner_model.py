"""
Owner database model.
"""
from datetime import datetime
from typing import Optional
from bson import ObjectId
from pydantic import BaseModel, Field, ConfigDict, EmailStr


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


class BusinessLocation(BaseModel):
    """Structured location information for a business."""
    address_line1: Optional[str] = None
    address_line2: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    postal_code: Optional[str] = None
    country: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None


class BusinessContact(BaseModel):
    """Primary contact information for a business."""
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    whatsapp: Optional[str] = None
    website: Optional[str] = None


class StorefrontInfo(BaseModel):
    """Hosted storefront metadata."""
    slug: str
    url: str
    published: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class BusinessProfile(BaseModel):
    """Business profile for an owner."""
    name: str
    slug: str
    description: Optional[str] = None
    category: Optional[str] = None
    logo_url: Optional[str] = None
    location: Optional[BusinessLocation] = None
    contact: Optional[BusinessContact] = None
    storefront: Optional[StorefrontInfo] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class OwnerOnboardingStatus(BaseModel):
    """Tracks onboarding completion for an owner."""
    completed: bool = False
    completed_at: Optional[datetime] = None
    storefront_url: Optional[str] = None
    storefront_slug: Optional[str] = None


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
    business_profile: Optional[BusinessProfile] = None
    onboarding: OwnerOnboardingStatus = Field(default_factory=OwnerOnboardingStatus)
    
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "firebase_uid": "firebase_uid_123",
                "email": "owner@example.com",
                "business_name": "My Shop",
                "phone": "+1234567890",
                "address": "123 Main St",
                "business_profile": {
                    "name": "My Shop",
                    "slug": "my-shop",
                    "description": "A curated selection of local goods",
                    "category": "Retail",
                    "logo_url": "https://res.cloudinary.com/...",
                    "location": {
                        "address_line1": "123 Main St",
                        "city": "Metropolis",
                        "country": "USA"
                    },
                    "contact": {
                        "name": "Jane Doe",
                        "email": "owner@example.com",
                        "phone": "+1234567890"
                    },
                    "storefront": {
                        "slug": "my-shop",
                        "url": "https://yourplatform.com/shop/my-shop",
                        "published": True
                    }
                },
                "onboarding": {
                    "completed": True,
                    "completed_at": "2024-01-01T12:00:00Z",
                    "storefront_url": "https://yourplatform.com/shop/my-shop",
                    "storefront_slug": "my-shop"
                }
            }
        }
    )

