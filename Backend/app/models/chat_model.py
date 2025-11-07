"""
Chat database model for AI agent conversations.
"""
from datetime import datetime
from typing import Optional
from bson import ObjectId
from pydantic import BaseModel, Field, ConfigDict
from app.models.owner_model import PyObjectId


class ChatMessage(BaseModel):
    """Chat message model."""
    role: str = Field(..., description="Message role: user or assistant")
    content: str = Field(..., description="Message content")
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class ChatModel(BaseModel):
    """Chat conversation database model."""
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    user_id: Optional[str] = Field(None, description="User Firebase UID (owner or customer)")
    user_type: str = Field(..., description="User type: owner or customer")
    owner_id: Optional[str] = Field(None, description="Owner Firebase UID (for customer chats)")
    messages: List[ChatMessage] = Field(default_factory=list, description="Chat messages")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "user_id": "firebase_uid_123",
                "user_type": "customer",
                "owner_id": "owner_uid_123",
                "messages": [
                    {
                        "role": "user",
                        "content": "What products do you have?"
                    },
                    {
                        "role": "assistant",
                        "content": "We have a wide range of products..."
                    }
                ]
            }
        }
    )

