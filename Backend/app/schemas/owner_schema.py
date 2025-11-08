"""
Owner Pydantic schemas for request/response validation.
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field
from app.models.owner_model import BusinessProfile


class BusinessLocation(BaseModel):
    """Structured business location details."""
    address_line1: Optional[str] = None
    address_line2: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    postal_code: Optional[str] = None
    country: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None


class BusinessContact(BaseModel):
    """Business contact information."""
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    whatsapp: Optional[str] = None
    website: Optional[str] = None


class Storefront(BaseModel):
    """Hosted storefront metadata."""
    slug: str
    url: str
    published: bool = True
    created_at: datetime
    updated_at: datetime


class BusinessProfileBase(BaseModel):
    """Shared business profile fields."""
    name: str
    description: Optional[str] = None
    category: Optional[str] = None
    logo_url: Optional[str] = None
    location: Optional[BusinessLocation] = None
    contact: Optional[BusinessContact] = None


class BusinessProfileResponse(BusinessProfileBase):
    """Business profile response schema."""
    slug: str
    storefront: Optional[Storefront] = None
    created_at: datetime
    updated_at: datetime


class OwnerOnboarding(BaseModel):
    """Owner onboarding status schema."""
    completed: bool = False
    completed_at: Optional[datetime] = None
    storefront_url: Optional[str] = None
    storefront_slug: Optional[str] = None


class OwnerBase(BaseModel):
    """Base owner schema."""
    email: EmailStr
    business_name: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    business_profile: Optional[BusinessProfile] = None
    onboarding: Optional[OwnerOnboarding] = None


class OwnerCreate(OwnerBase):
    """Schema for creating an owner."""
    firebase_uid: Optional[str] = None
    business_profile: Optional[BusinessProfileBase] = None


class OwnerUpdate(BaseModel):
    """Schema for updating an owner."""
    business_name: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    business_profile: Optional[BusinessProfileBase] = None


class OwnerResponse(OwnerBase):
    """Schema for owner response."""
    id: str
    firebase_uid: str
    created_at: datetime
    updated_at: datetime
    business_profile: Optional[BusinessProfileResponse] = None
    onboarding: Optional[OwnerOnboarding] = None
    
    class Config:
        from_attributes = True

