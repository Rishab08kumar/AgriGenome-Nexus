from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    FIREBASE_CREDENTIALS_PATH: Optional[str] = None
    FIREBASE_DATABASE_URL: Optional[str] = None
    FIREBASE_PROJECT_ID: Optional[str] = None
    API_SECRET_KEY: Optional[str] = "default_secret"

    class Config:
        env_file = ".env"

settings = Settings()
