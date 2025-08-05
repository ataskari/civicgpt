"""
Configuration settings for CivicGPT application.
"""
import os
from typing import Optional
from pydantic import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # OpenAI Configuration
    openai_api_key: str
    openai_model: str = "gpt-3.5-turbo"
    openai_max_tokens: int = 1000
    openai_temperature: float = 0.3
    
    # Application Configuration
    app_name: str = "CivicGPT"
    app_version: str = "1.0.0"
    environment: str = "development"
    debug: bool = True
    
    # API Configuration
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    api_reload: bool = True
    
    # Frontend Configuration
    frontend_host: str = "localhost"
    frontend_port: int = 8501
    
    # Logging Configuration
    log_level: str = "INFO"
    log_format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # Analysis Configuration
    max_post_length: int = 280  # Twitter character limit
    analysis_timeout: int = 10  # seconds
    
    # Rate Limiting
    rate_limit_per_minute: int = 60
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


# Global settings instance
settings = Settings()


def get_settings() -> Settings:
    """Get application settings."""
    return settings


# Environment-specific configurations
def is_development() -> bool:
    """Check if running in development mode."""
    return settings.environment.lower() == "development"


def is_production() -> bool:
    """Check if running in production mode."""
    return settings.environment.lower() == "production"


# API URLs
def get_api_url() -> str:
    """Get the API base URL."""
    return f"http://{settings.api_host}:{settings.api_port}"


def get_frontend_url() -> str:
    """Get the frontend URL."""
    return f"http://{settings.frontend_host}:{settings.frontend_port}" 