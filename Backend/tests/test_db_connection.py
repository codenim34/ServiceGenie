"""
MongoDB Connection Test Script
Run this to verify your MongoDB Atlas connection is working.
"""

import asyncio
import os
import pytest
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.config import settings

async def test_mongodb_connection():
    """Test MongoDB connection and basic operations."""
    
    print("=" * 60)
    print("🔍 ServiceGenie - MongoDB Connection Test")
    print("=" * 60)
    print()
    
    try:
        # Display connection info (hide password)
        mongo_url_safe = settings.MONGODB_URL.split('@')[1] if '@' in settings.MONGODB_URL else settings.MONGODB_URL
        print(f"📡 Connecting to: ...@{mongo_url_safe}")
        print(f"📊 Database name: {settings.DATABASE_NAME}")
        print()
        
        # Create client
        client = AsyncIOMotorClient(settings.MONGODB_URL)
        
        # Test connection with ping
        print("⏳ Testing connection...")
        await client.admin.command('ping')
        print("✅ Connection successful! MongoDB is responding.")
        print()
        
        # Get database
        db = client[settings.DATABASE_NAME]
        
        # List existing collections
        print("📂 Existing collections:")
        collections = await db.list_collection_names()
        if collections:
            for collection in collections:
                count = await db[collection].count_documents({})
                print(f"   - {collection}: {count} documents")
        else:
            print("   (No collections yet - database is empty)")
        print()
        
        # Test write operation
        print("✍️  Testing write operation...")
        test_collection = db.test_connection
        test_doc = {
            "test": "ServiceGenie Connection Test",
            "timestamp": datetime.utcnow(),
            "status": "success"
        }
        result = await test_collection.insert_one(test_doc)
        print(f"✅ Write successful! Document ID: {result.inserted_id}")
        print()
        
        # Test read operation
        print("📖 Testing read operation...")
        retrieved_doc = await test_collection.find_one({"_id": result.inserted_id})
        print(f"✅ Read successful! Retrieved: {retrieved_doc['test']}")
        print()
        
        # Cleanup test document
        print("🧹 Cleaning up test document...")
        await test_collection.delete_one({"_id": result.inserted_id})
        print("✅ Cleanup successful!")
        print()
        
        # Display database info
        print("📊 Database Statistics:")
        stats = await db.command("dbStats")
        print(f"   - Collections: {stats.get('collections', 0)}")
        print(f"   - Data Size: {stats.get('dataSize', 0)} bytes")
        print(f"   - Storage Size: {stats.get('storageSize', 0)} bytes")
        print()
        
        print("=" * 60)
        print("🎉 All tests passed! Your MongoDB connection is working perfectly!")
        print("=" * 60)
        print()
        print("Next steps:")
        print("1. Run: python scripts/seed_db.py (to add sample data)")
        print("2. Run: uvicorn main:app --reload (to start the API)")
        print()
        
        # Close connection
        client.close()
        return True
        
    except Exception as e:
        print("=" * 60)
        print("❌ Connection Test Failed!")
        print("=" * 60)
        print()
        print(f"Error: {str(e)}")
        print()
        print("Common issues:")
        print("1. Check your MONGODB_URL in .env file")
        print("2. Verify your MongoDB Atlas cluster is running")
        print("3. Check your IP address is whitelisted in MongoDB Atlas")
        print("4. Verify username and password are correct")
        print("5. Check network connectivity")
        print()
        return False

if __name__ == "__main__":
    # Allow running standalone, but pytest should skip this module by default.
    success = asyncio.run(test_mongodb_connection())
    sys.exit(0 if success else 1)

# Skip heavy integration test unless explicitly enabled
if not os.environ.get("RUN_INTEGRATION"):
    pytest.skip("Skipping MongoDB integration test (set RUN_INTEGRATION=1 to enable)", allow_module_level=True)
