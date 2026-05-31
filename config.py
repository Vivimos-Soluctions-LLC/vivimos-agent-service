from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application configuration from environment variables."""

    # Database
    database_url: str
    sqlalchemy_echo: bool = False

    # API Keys
    anthropic_api_key: str
    openai_api_key: str

    # FastAPI
    environment: str = "development"
    debug: bool = True
    api_title: str = "Vivimos Agent Service"
    api_version: str = "0.1.0"

    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
