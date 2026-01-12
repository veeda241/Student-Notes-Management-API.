"""
Application configuration settings.
Uses pydantic-settings for environment variable management.
"""

from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Application
    APP_NAME: str = "Student Notes Management API"
    APP_VERSION: str = "1.0.0"
    APP_DESCRIPTION: str = "A clean, modular API for managing student notes"
    DEBUG: bool = True
    
    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # Database (ready for MySQL integration)
    DATABASE_URL: str = "sqlite:///./notes.db"  # Change to MySQL when ready
    # Example MySQL: "mysql+pymysql://user:password@localhost:3306/notes_db"
    
    # API Settings
    API_V1_PREFIX: str = "/api/v1"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()


settings = get_settings()
