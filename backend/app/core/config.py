from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # Project settings
    PROJECT_NAME: str = "Task Notification System"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # Database configuration
    DATABASE_URL: str
    
    # Redis configuration
    REDIS_URL: str
    
    # Security settings
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    class Config:
        env_file = ".env"

settings = Settings()