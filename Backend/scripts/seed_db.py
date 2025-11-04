"""
Database seeder script to populate MongoDB with sample data.
Run this script to add initial products and categories.
"""

import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.config import settings

# Sample Categories
CATEGORIES = [
    {
        "name": "Electronics",
        "slug": "electronics",
        "description": "Latest electronic gadgets and devices",
        "icon": "Laptop"
    },
    {
        "name": "Fashion",
        "slug": "fashion",
        "description": "Trendy clothing and accessories",
        "icon": "Shirt"
    },
    {
        "name": "Watches",
        "slug": "watches",
        "description": "Premium and casual watches",
        "icon": "Watch"
    },
    {
        "name": "Audio",
        "slug": "audio",
        "description": "Headphones, speakers, and audio equipment",
        "icon": "Headphones"
    },
    {
        "name": "Home & Living",
        "slug": "home-living",
        "description": "Home decor and living essentials",
        "icon": "Home"
    },
    {
        "name": "Gifts",
        "slug": "gifts",
        "description": "Perfect gifts for every occasion",
        "icon": "Gift"
    }
]

# Sample Products
PRODUCTS = [
    # Electronics
    {
        "name": "Wireless Noise-Cancelling Headphones",
        "description": "Premium over-ear headphones with active noise cancellation, 30-hour battery life, and superior sound quality.",
        "price": 149.99,
        "originalPrice": 249.99,
        "category": "electronics",
        "images": ["https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=500"],
        "stock": 50,
        "rating": 4.7,
        "reviews": 342,
        "tags": ["wireless", "bluetooth", "audio", "premium"],
        "specifications": {
            "battery": "30 hours",
            "connectivity": "Bluetooth 5.0",
            "weight": "250g"
        },
        "featured": True
    },
    {
        "name": "Smart Watch Pro",
        "description": "Advanced smartwatch with fitness tracking, heart rate monitor, and 5-day battery life.",
        "price": 299.99,
        "originalPrice": 399.99,
        "category": "watches",
        "images": ["https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=500"],
        "stock": 35,
        "rating": 4.5,
        "reviews": 218,
        "tags": ["smartwatch", "fitness", "health"],
        "specifications": {
            "display": "1.4 inch AMOLED",
            "battery": "5 days",
            "waterproof": "IP68"
        },
        "featured": True
    },
    {
        "name": "Laptop Backpack",
        "description": "Durable and stylish laptop backpack with multiple compartments and USB charging port.",
        "price": 49.99,
        "originalPrice": 79.99,
        "category": "fashion",
        "images": ["https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=500"],
        "stock": 100,
        "rating": 4.3,
        "reviews": 156,
        "tags": ["backpack", "laptop", "travel"],
        "specifications": {
            "capacity": "20L",
            "material": "Waterproof Nylon"
        },
        "featured": False
    },
    # Audio
    {
        "name": "Portable Bluetooth Speaker",
        "description": "Compact wireless speaker with 360° sound, waterproof design, and 12-hour playtime.",
        "price": 79.99,
        "originalPrice": 129.99,
        "category": "audio",
        "images": ["https://images.unsplash.com/photo-1608043152269-423dbba4e7e1?w=500"],
        "stock": 75,
        "rating": 4.6,
        "reviews": 289,
        "tags": ["bluetooth", "speaker", "portable", "waterproof"],
        "specifications": {
            "battery": "12 hours",
            "waterproof": "IPX7",
            "output": "20W"
        },
        "featured": True
    },
    {
        "name": "Premium Leather Wallet",
        "description": "Handcrafted genuine leather wallet with RFID protection and multiple card slots.",
        "price": 39.99,
        "originalPrice": 69.99,
        "category": "fashion",
        "images": ["https://images.unsplash.com/photo-1627123424574-724758594e93?w=500"],
        "stock": 120,
        "rating": 4.8,
        "reviews": 412,
        "tags": ["wallet", "leather", "accessories", "RFID"],
        "specifications": {
            "material": "Genuine Leather",
            "slots": "8 card slots"
        },
        "featured": False
    },
    # Home & Living
    {
        "name": "Smart LED Desk Lamp",
        "description": "Adjustable desk lamp with touch controls, multiple brightness levels, and USB charging port.",
        "price": 34.99,
        "originalPrice": 54.99,
        "category": "home-living",
        "images": ["https://images.unsplash.com/photo-1507473885765-e6ed057f782c?w=500"],
        "stock": 85,
        "rating": 4.4,
        "reviews": 167,
        "tags": ["lamp", "LED", "desk", "smart"],
        "specifications": {
            "brightness": "5 levels",
            "color temp": "2700K-6500K"
        },
        "featured": False
    },
    {
        "name": "Wireless Gaming Mouse",
        "description": "High-precision gaming mouse with customizable RGB lighting and 16000 DPI sensor.",
        "price": 59.99,
        "originalPrice": 89.99,
        "category": "electronics",
        "images": ["https://images.unsplash.com/photo-1527814050087-3793815479db?w=500"],
        "stock": 60,
        "rating": 4.7,
        "reviews": 234,
        "tags": ["gaming", "mouse", "wireless", "RGB"],
        "specifications": {
            "DPI": "16000",
            "battery": "70 hours",
            "buttons": "6 programmable"
        },
        "featured": True
    },
    {
        "name": "Minimalist Wall Clock",
        "description": "Modern silent wall clock with minimalist design, perfect for any room.",
        "price": 24.99,
        "originalPrice": 44.99,
        "category": "home-living",
        "images": ["https://images.unsplash.com/photo-1563861826100-9cb868fdbe1c?w=500"],
        "stock": 95,
        "rating": 4.2,
        "reviews": 89,
        "tags": ["clock", "wall", "decor", "minimalist"],
        "specifications": {
            "diameter": "12 inches",
            "silent": "Yes"
        },
        "featured": False
    }
]

async def seed_database():
    """Seed the database with sample data."""
    client = AsyncIOMotorClient(settings.MONGODB_URL)
    db = client[settings.DATABASE_NAME]
    
    print("🌱 Seeding database...")
    
    try:
        # Clear existing data
        await db.categories.delete_many({})
        await db.products.delete_many({})
        print("✅ Cleared existing data")
        
        # Insert categories
        for category in CATEGORIES:
            category["createdAt"] = datetime.utcnow()
            category["updatedAt"] = datetime.utcnow()
        
        result = await db.categories.insert_many(CATEGORIES)
        print(f"✅ Inserted {len(result.inserted_ids)} categories")
        
        # Insert products
        for product in PRODUCTS:
            product["createdAt"] = datetime.utcnow()
            product["updatedAt"] = datetime.utcnow()
            
            # Calculate discount
            if product.get("originalPrice"):
                product["discount"] = round(
                    ((product["originalPrice"] - product["price"]) / product["originalPrice"]) * 100, 2
                )
        
        result = await db.products.insert_many(PRODUCTS)
        print(f"✅ Inserted {len(result.inserted_ids)} products")
        
        print("\n🎉 Database seeding completed successfully!")
        print(f"📊 Total categories: {len(CATEGORIES)}")
        print(f"📦 Total products: {len(PRODUCTS)}")
        
    except Exception as e:
        print(f"❌ Error seeding database: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    asyncio.run(seed_database())
