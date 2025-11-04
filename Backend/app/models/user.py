from pydantic import BaseModel, Field, EmailStr
from typing import Optional, Literal
from datetime import datetime
from bson import ObjectId

class PyObjectId(ObjectId):
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

class UserBase(BaseModel):
    email: EmailStr
    displayName: Optional[str] = None
    photoURL: Optional[str] = None

class UserCreate(UserBase):
    uid: str

class UserUpdate(BaseModel):
    displayName: Optional[str] = None
    photoURL: Optional[str] = None

class UserInDB(UserBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    uid: str
    role: Literal["customer", "admin"] = "customer"
    createdAt: datetime = Field(default_factory=datetime.utcnow)
    updatedAt: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "displayName": "John Doe",
                "uid": "firebase-uid-123",
                "role": "customer"
            }
        }

class UserResponse(BaseModel):
    id: str = Field(alias="_id")
    email: EmailStr
    displayName: Optional[str] = None
    photoURL: Optional[str] = None
    role: str
    createdAt: datetime

    class Config:
        populate_by_name = True
