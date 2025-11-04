from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings
from typing import Optional

class Database:
    client: Optional[AsyncIOMotorClient] = None
    
db = Database()

async def connect_to_mongo():
    """Create database connection."""
    db.client = AsyncIOMotorClient(settings.MONGODB_URL)
    print("✅ Connected to MongoDB")

async def close_mongo_connection():
    """Close database connection."""
    if db.client:
        db.client.close()
        print("❌ Closed connection to MongoDB")

def get_database():
    """Get database instance."""
    return db.client[settings.DATABASE_NAME]
