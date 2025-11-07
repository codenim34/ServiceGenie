"""
Owner Pydantic schemas for request/response validation.
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field


class OwnerBase(BaseModel):
    """Base owner schema."""
    email: EmailStr
    business_name: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None


class OwnerCreate(OwnerBase):
    """Schema for creating an owner."""
    firebase_uid: str


class OwnerUpdate(BaseModel):
    """Schema for updating an owner."""
    business_name: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None


class OwnerResponse(OwnerBase):
    """Schema for owner response."""
    id: str
    firebase_uid: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

