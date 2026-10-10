"""Configuration for the application."""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings."""
    
    # API
    api_title: str = "InterleaveLab - Concurrency Bug Detection"
    api_version: str = "1.0.0"
    api_description: str = "Detect race conditions in concurrent API requests"
    
    # Environment
    environment: str = "development"
    debug: bool = True
    
    # Database
    database_url: Optional[str] = None
    use_in_memory: bool = True
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Create global settings instance
settings = Settings()
