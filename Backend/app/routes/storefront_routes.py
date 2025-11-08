"""Public storefront routes."""
from typing import Any, Dict

from fastapi import APIRouter, HTTPException

from app.core.db import get_database


router = APIRouter(prefix="/storefronts", tags=["storefronts"])


def _serialize_product(product: Dict[str, Any]) -> Dict[str, Any]:
    serialized = product.copy()
    serialized["id"] = str(serialized["_id"])
    serialized.pop("_id", None)
    return serialized


@router.get("/{slug}", response_model=dict)
async def get_storefront(slug: str):
    """Return storefront data by slug."""
    db = get_database()
    owners_collection = db.owners
    products_collection = db.products

    owner = await owners_collection.find_one({"business_profile.slug": slug})
    if not owner:
        raise HTTPException(status_code=404, detail="Storefront not found")

    onboarding = owner.get("onboarding", {}) or {}
    if not onboarding.get("completed"):
        raise HTTPException(status_code=404, detail="Storefront not published yet")

    products_cursor = products_collection.find({
        "owner_id": owner["firebase_uid"],
        "is_available": True
    })

    products = [_serialize_product(product) async for product in products_cursor]

    business_profile = owner.get("business_profile", {}) or {}
    storefront = business_profile.get("storefront", {}) or {}

    response = {
        "business": {
            "name": business_profile.get("name", owner.get("business_name")),
            "description": business_profile.get("description"),
            "category": business_profile.get("category"),
            "logo_url": business_profile.get("logo_url"),
            "location": business_profile.get("location"),
            "contact": business_profile.get("contact"),
            "storefront": {
                "slug": storefront.get("slug", slug),
                "url": onboarding.get("storefront_url"),
                "published": storefront.get("published", True),
                "updated_at": storefront.get("updated_at"),
            },
        },
        "products": products,
    }

    return response


