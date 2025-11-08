"""Owner routes for owner management and onboarding."""
import json
from datetime import datetime
from typing import Any, Dict, Optional

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form

from app.routes.auth_routes import get_current_user
from app.core.db import get_database
from app.core.config import settings
from app.schemas.owner_schema import OwnerCreate, OwnerUpdate, OwnerResponse
from app.services.order_service import get_owner_analytics
from app.utils.cloudinary_utils import upload_image_from_bytes
from app.utils.slug_utils import generate_unique_slug


router = APIRouter(prefix="/owners", tags=["owners"])


def _serialize_owner(owner: Dict[str, Any]) -> Dict[str, Any]:
    """Convert Mongo document to API-friendly dict."""
    serialized = owner.copy()
    serialized["id"] = str(serialized["_id"])
    serialized.pop("_id", None)
    return serialized


@router.post("", response_model=OwnerResponse, status_code=201)
async def create_owner(
    owner_data: OwnerCreate,
    current_user: dict = Depends(get_current_user)
):
    """Create or update owner profile stub on registration."""
    db = get_database()
    owners_collection = db.owners

    existing_owner = await owners_collection.find_one({"firebase_uid": current_user["uid"]})

    owner_payload = owner_data.model_dump(
        exclude_none=True,
        exclude={"firebase_uid", "business_profile"}
    )

    owner_payload["firebase_uid"] = current_user["uid"]
    owner_payload["email"] = current_user.get("email") or owner_data.email
    owner_payload["updated_at"] = datetime.utcnow()

    if existing_owner:
        await owners_collection.update_one(
            {"firebase_uid": current_user["uid"]},
            {"$set": owner_payload}
        )
        owner = await owners_collection.find_one({"firebase_uid": current_user["uid"]})
    else:
        owner_payload["created_at"] = datetime.utcnow()
        owner_payload.setdefault("business_profile", None)
        owner_payload.setdefault(
            "onboarding",
            {
                "completed": False,
                "completed_at": None,
                "storefront_url": None,
                "storefront_slug": None,
            }
        )
        result = await owners_collection.insert_one(owner_payload)
        owner = await owners_collection.find_one({"_id": result.inserted_id})

    return _serialize_owner(owner)


@router.post("/onboarding", response_model=OwnerResponse)
async def complete_business_onboarding(
    business_name: str = Form(...),
    category: str = Form(...),
    description: Optional[str] = Form(None),
    location: Optional[str] = Form(None),
    contact: Optional[str] = Form(None),
    logo: Optional[UploadFile] = File(None),
    current_user: dict = Depends(get_current_user)
):
    """Complete business onboarding for an owner."""
    db = get_database()
    owners_collection = db.owners

    owner = await owners_collection.find_one({"firebase_uid": current_user["uid"]})
    if not owner:
        raise HTTPException(status_code=404, detail="Owner profile not found")

    def _parse_json_field(raw_value: Optional[str], field_name: str) -> Optional[Dict[str, Any]]:
        if not raw_value:
            return None
        try:
            return json.loads(raw_value)
        except json.JSONDecodeError:
            raise HTTPException(status_code=400, detail=f"Invalid JSON payload for {field_name}")

    location_data = _parse_json_field(location, "location")
    contact_data = _parse_json_field(contact, "contact")

    logo_url = owner.get("business_profile", {}).get("logo_url")
    if logo:
        logo_bytes = await logo.read()
        uploaded_logo = await upload_image_from_bytes(
            logo_bytes,
            logo.filename or "business-logo.png",
            folder="storefronts"
        )
        if uploaded_logo:
            logo_url = uploaded_logo

    existing_profile = owner.get("business_profile", {}) or {}
    slug = existing_profile.get("slug")
    name_changed = existing_profile.get("name") != business_name
    if not slug or name_changed:
        slug = await generate_unique_slug(business_name, owners_collection, owner.get("_id"))

    base_url = settings.STOREFRONT_BASE_URL.rstrip("/") if settings.STOREFRONT_BASE_URL else ""
    storefront_url = f"{base_url}/shop/{slug}" if base_url else f"/shop/{slug}"

    now = datetime.utcnow()
    storefront_meta = existing_profile.get("storefront", {})
    storefront_info = {
        "slug": slug,
        "url": storefront_url,
        "published": True,
        "created_at": storefront_meta.get("created_at", now),
        "updated_at": now,
    }

    business_profile = {
        "name": business_name,
        "slug": slug,
        "description": description or existing_profile.get("description"),
        "category": category or existing_profile.get("category"),
        "logo_url": logo_url or existing_profile.get("logo_url"),
        "location": location_data if location_data is not None else existing_profile.get("location"),
        "contact": contact_data if contact_data is not None else existing_profile.get("contact"),
        "storefront": storefront_info,
        "created_at": existing_profile.get("created_at", now),
        "updated_at": now,
    }

    onboarding_state = owner.get("onboarding", {}) or {}
    onboarding_data = {
        "completed": True,
        "completed_at": onboarding_state.get("completed_at") or now,
        "storefront_url": storefront_url,
        "storefront_slug": slug,
    }

    update_fields: Dict[str, Any] = {
        "business_name": business_name,
        "business_profile": business_profile,
        "onboarding": onboarding_data,
        "updated_at": now,
    }

    if contact_data and contact_data.get("phone"):
        update_fields["phone"] = contact_data["phone"]
    if location_data and location_data.get("address_line1"):
        update_fields["address"] = location_data["address_line1"]

    await owners_collection.update_one(
        {"firebase_uid": current_user["uid"]},
        {"$set": update_fields}
    )

    owner = await owners_collection.find_one({"firebase_uid": current_user["uid"]})
    return _serialize_owner(owner)


@router.get("/me", response_model=OwnerResponse)
async def get_owner_profile(current_user: dict = Depends(get_current_user)):
    """Get the current owner's profile."""
    db = get_database()
    owners_collection = db.owners

    owner = await owners_collection.find_one({"firebase_uid": current_user["uid"]})
    if not owner:
        raise HTTPException(status_code=404, detail="Owner profile not found")

    return _serialize_owner(owner)


@router.put("/me", response_model=OwnerResponse)
async def update_owner_profile(
    owner_data: OwnerUpdate,
    current_user: dict = Depends(get_current_user)
):
    """Update current owner profile."""
    db = get_database()
    owners_collection = db.owners

    update_data = owner_data.model_dump(exclude_unset=True, exclude_none=True)
    update_data["updated_at"] = datetime.utcnow()

    result = await owners_collection.update_one(
        {"firebase_uid": current_user["uid"]},
        {"$set": update_data}
    )

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Owner profile not found")

    owner = await owners_collection.find_one({"firebase_uid": current_user["uid"]})
    return _serialize_owner(owner)


@router.get("/me/analytics", response_model=dict)
async def get_analytics(current_user: dict = Depends(get_current_user)):
    """Get owner analytics."""
    owner_id = current_user["uid"]
    analytics = await get_owner_analytics(owner_id)
    return analytics

