"""Utility helpers for generating slugs."""
import re
from typing import Optional

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorCollection


def slugify(value: str) -> str:
    """Create a URL-friendly slug from a string."""
    value = value.lower().strip()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    value = re.sub(r"-+", "-", value)
    value = value.strip("-")
    return value or "storefront"


async def generate_unique_slug(
    name: str,
    collection: AsyncIOMotorCollection,
    current_owner_id: Optional[ObjectId] = None
) -> str:
    """Generate a unique slug for a business name within the provided collection."""
    base_slug = slugify(name)
    candidate = base_slug
    suffix = 1

    while True:
        query = {"business_profile.slug": candidate}
        if current_owner_id:
            query["_id"] = {"$ne": current_owner_id}

        existing = await collection.find_one(query, {"_id": 1})
        if not existing:
            return candidate

        candidate = f"{base_slug}-{suffix}"
        suffix += 1


