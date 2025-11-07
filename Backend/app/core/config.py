"""
Application configuration settings.
"""
from pydantic_settings import BaseSettings
from typing import List, Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # MongoDB
    MONGO_URI: str
    DATABASE_NAME: str = "servicegenie"
    
    # Firebase
    FIREBASE_PROJECT_ID: str
    FIREBASE_CREDENTIAL_PATH: str
    
    # Cloudinary
    CLOUDINARY_API_KEY: Optional[str] = None
    CLOUDINARY_API_SECRET: Optional[str] = None
    CLOUDINARY_CLOUD_NAME: Optional[str] = None
    
    # OpenAI (for AI agent)
    OPENAI_API_KEY: Optional[str] = None
    
    # API
    API_V1_PREFIX: str = "/api/v1"
    SECRET_KEY: str = "dev-secret-key-change-in-production"
    
    # CORS
    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:3001"]
    
    # Environment
    ENVIRONMENT: str = "development"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
