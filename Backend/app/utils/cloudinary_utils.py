"""
Cloudinary utility functions for image uploads.
"""
import cloudinary
import cloudinary.uploader
from app.core.config import settings
from typing import Optional
import os


def initialize_cloudinary():
    """Initialize Cloudinary configuration."""
    if all([
        settings.CLOUDINARY_CLOUD_NAME,
        settings.CLOUDINARY_API_KEY,
        settings.CLOUDINARY_API_SECRET
    ]):
        cloudinary.config(
            cloud_name=settings.CLOUDINARY_CLOUD_NAME,
            api_key=settings.CLOUDINARY_API_KEY,
            api_secret=settings.CLOUDINARY_API_SECRET
        )
    else:
        print("⚠️ Cloudinary credentials not configured. Image uploads will be disabled.")


async def upload_image(file_path: str, folder: str = "products") -> Optional[str]:
    """
    Upload an image to Cloudinary.
    
    Args:
        file_path: Path to the image file
        folder: Cloudinary folder name
        
    Returns:
        str: Image URL or None if upload fails
    """
    try:
        initialize_cloudinary()
        
        result = cloudinary.uploader.upload(
            file_path,
            folder=folder,
            resource_type="image"
        )
        return result.get("secure_url")
    except Exception as e:
        print(f"Error uploading image to Cloudinary: {e}")
        return None


async def upload_image_from_bytes(file_bytes: bytes, filename: str, folder: str = "products") -> Optional[str]:
    """
    Upload an image to Cloudinary from bytes.
    
    Args:
        file_bytes: Image file bytes
        filename: Original filename
        folder: Cloudinary folder name
        
    Returns:
        str: Image URL or None if upload fails
    """
    try:
        initialize_cloudinary()
        
        result = cloudinary.uploader.upload(
            file_bytes,
            folder=folder,
            resource_type="image",
            filename=filename
        )
        return result.get("secure_url")
    except Exception as e:
        print(f"Error uploading image to Cloudinary: {e}")
        return None


def delete_image(public_id: str) -> bool:
    """
    Delete an image from Cloudinary.
    
    Args:
        public_id: Cloudinary public ID
        
    Returns:
        bool: True if deleted successfully
    """
    try:
        initialize_cloudinary()
        result = cloudinary.uploader.destroy(public_id)
        return result.get("result") == "ok"
    except Exception as e:
        print(f"Error deleting image from Cloudinary: {e}")
        return False

