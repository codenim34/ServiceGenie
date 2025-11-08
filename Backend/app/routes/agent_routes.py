"""
AI agent routes for chat functionality.
"""
from fastapi import APIRouter, Depends, HTTPException
from typing import Optional
from app.routes.auth_routes import get_current_user, get_optional_user
from app.schemas.chat_schema import ChatMessageCreate, ChatResponse, ChatHistoryResponse
from app.services.ai_service import process_chat_message
from app.core.db import get_database
from datetime import datetime
from bson import ObjectId

router = APIRouter(prefix="/agent", tags=["agent"])


@router.post("/chat", response_model=ChatResponse)
async def chat_with_agent(
    message_data: ChatMessageCreate,
    current_user: Optional[dict] = Depends(get_optional_user)
):
    """
    Chat with AI agent.
    
    Args:
        message_data: Chat message data
        current_user: Current authenticated user (optional)
        
    Returns:
        ChatResponse: AI agent response
    """
    user_id = current_user["uid"] if current_user else None
    user_type = "owner" if current_user and message_data.owner_id is None else "customer"
    owner_id = message_data.owner_id
    
    # Process message with AI service
    response = await process_chat_message(
        message=message_data.content,
        owner_id=owner_id,
        user_type=user_type
    )
    
    # Save chat history if user is authenticated
    if user_id:
        db = get_database()
        chats_collection = db.chats
        
        # Find or create chat session
        chat = await chats_collection.find_one({
            "user_id": user_id,
            "owner_id": owner_id or None
        })
        
        if chat:
            # Update existing chat
            await chats_collection.update_one(
                {"_id": chat["_id"]},
                {
                    "$push": {
                        "messages": {
                            "$each": [
                                {
                                    "role": "user",
                                    "content": message_data.content,
                                    "timestamp": datetime.utcnow()
                                },
                                {
                                    "role": "assistant",
                                    "content": response.reply,
                                    "timestamp": datetime.utcnow()
                                }
                            ]
                        }
                    },
                    "$set": {"updated_at": datetime.utcnow()}
                }
            )
        else:
            # Create new chat
            chat_dict = {
                "user_id": user_id,
                "user_type": user_type,
                "owner_id": owner_id,
                "messages": [
                    {
                        "role": "user",
                        "content": message_data.content,
                        "timestamp": datetime.utcnow()
                    },
                    {
                        "role": "assistant",
                        "content": response.reply,
                        "timestamp": datetime.utcnow()
                    }
                ],
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            }
            await chats_collection.insert_one(chat_dict)
    
    return response


@router.get("/chat/history", response_model=list)
async def get_chat_history(
    owner_id: Optional[str] = None,
    cursor: Optional[str] = None,
    limit: int = 20,
    current_user: Optional[dict] = Depends(get_optional_user)
):
    """
    Get chat history for current user with cursor-based pagination.
    
    Args:
        owner_id: Optional owner ID to filter chats
        cursor: Cursor for pagination (timestamp of last message)
        limit: Number of messages to return
        current_user: Current authenticated user
        
    Returns:
        List[dict]: Chat history
    """
    if not current_user:
        raise HTTPException(status_code=401, detail="Authentication required")
    
    db = get_database()
    chats_collection = db.chats
    
    # Build query
    query = {"user_id": current_user["uid"]}
    if owner_id:
        query["owner_id"] = owner_id
    if cursor:
        query["updated_at"] = {"$lt": datetime.fromisoformat(cursor)}
    
    # Get paginated results with lean projection
    cursor = chats_collection.find(
        query,
        projection={
            "messages": {"$slice": -limit},  # Get only recent messages
            "user_id": 1,
            "owner_id": 1,
            "updated_at": 1
        }
    ).sort("updated_at", -1).limit(limit)
    
    chats = await cursor.to_list(length=limit)
    
    # Transform for response
    for chat in chats:
        chat["id"] = str(chat["_id"])
        del chat["_id"]
        
        # Add cursor for next page if there are more messages
        if len(chats) == limit:
            chat["next_cursor"] = chat["updated_at"].isoformat()
    
    return chats

