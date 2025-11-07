"""
Chat Pydantic schemas for request/response validation.
"""
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field


class ChatMessageCreate(BaseModel):
    """Schema for creating a chat message."""
    content: str = Field(..., min_length=1)
    owner_id: Optional[str] = None  # Required for customer chats


class ChatMessageResponse(BaseModel):
    """Schema for chat message response."""
    role: str
    content: str
    timestamp: datetime


class ChatResponse(BaseModel):
    """Schema for chat response from AI agent."""
    reply: str
    products: List[dict] = Field(default_factory=list)


class ChatHistoryResponse(BaseModel):
    """Schema for chat history response."""
    id: str
    user_id: Optional[str] = None
    user_type: str
    owner_id: Optional[str] = None
    messages: List[ChatMessageResponse]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

