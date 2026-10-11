"""Configuration settings for InterleaveLab."""
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application configuration."""
    
    api_title: str = "InterleaveLab"
    api_version: str = "1.0.0"
    api_description: str = "Concurrency bug detection for backend APIs"
    
    environment: str = "development"
    debug: bool = True
    
    class Config:
        env_file = ".env"


settings = Settings()
