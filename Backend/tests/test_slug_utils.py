"""Tests for slug utility helpers."""
import pytest

from app.utils.slug_utils import generate_unique_slug, slugify


class FakeCollection:
    """Simple async collection stub for slug lookups."""

    def __init__(self, existing_slugs: set[str]):
        self._existing = existing_slugs

    async def find_one(self, query, projection=None):  # pragma: no cover - simple stub
        slug = query.get("business_profile.slug")
        if slug in self._existing:
            return {"_id": object()}
        return None


def test_slugify_basic():
    assert slugify("My Cool Shop!") == "my-cool-shop"


@pytest.mark.asyncio
async def test_generate_unique_slug_appends_suffix():
    collection = FakeCollection({"my-shop", "my-shop-1"})
    slug = await generate_unique_slug("My Shop", collection)
    assert slug == "my-shop-2"


@pytest.mark.asyncio
async def test_generate_unique_slug_ignores_current_owner():
    class OwnerAwareCollection(FakeCollection):
        async def find_one(self, query, projection=None):
            slug = query.get("business_profile.slug")
            owner_filter = query.get("_id", {}).get("$ne")
            if slug == "existing-shop" and owner_filter:
                return None
            return await super().find_one(query, projection)

    collection = OwnerAwareCollection({"existing-shop"})
    slug = await generate_unique_slug("Existing Shop", collection, object())
    assert slug == "existing-shop"


