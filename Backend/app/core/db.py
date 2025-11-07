"""
MongoDB database connection using Motor (async driver).
"""
from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings
from typing import Optional


class Database:
    """Database connection manager."""
    client: Optional[AsyncIOMotorClient] = None


db = Database()


async def connect_to_mongo():
    """Create database connection."""
    if db.client is None:
        db.client = AsyncIOMotorClient(settings.MONGO_URI)
        print("✅ Connected to MongoDB")
    return db.client


async def close_mongo_connection():
    """Close database connection."""
    if db.client:
        db.client.close()
        print("❌ Closed MongoDB connection")


def get_database():
    """Get database instance."""
    if db.client is None:
        raise RuntimeError("Database not connected. Call connect_to_mongo() first.")
    return db.client[settings.DATABASE_NAME]

