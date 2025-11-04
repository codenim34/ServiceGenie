from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    # MongoDB
    MONGODB_URL: str
    DATABASE_NAME: str
    
    # Firebase
    FIREBASE_CREDENTIALS_PATH: str
    
    # API
    API_V1_PREFIX: str = "/api"
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # CORS
    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000"]
    
    # Stripe
    STRIPE_SECRET_KEY: str
    STRIPE_WEBHOOK_SECRET: str
    
    # Environment
    ENVIRONMENT: str = "development"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

    @property
    def is_development(self) -> bool:
        return self.ENVIRONMENT == "development"

settings = Settings()
