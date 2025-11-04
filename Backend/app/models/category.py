from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from bson import ObjectId
from app.models.user import PyObjectId

class CategoryBase(BaseModel):
    name: str
    slug: str
    description: Optional[str] = None
    image: Optional[str] = None
    icon: Optional[str] = None

class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    slug: Optional[str] = None
    description: Optional[str] = None
    image: Optional[str] = None
    icon: Optional[str] = None

class CategoryInDB(CategoryBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    createdAt: datetime = Field(default_factory=datetime.utcnow)
    updatedAt: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class CategoryResponse(BaseModel):
    id: str = Field(alias="_id")
    name: str
    slug: str
    description: Optional[str] = None
    image: Optional[str] = None
    icon: Optional[str] = None

    class Config:
        populate_by_name = True
