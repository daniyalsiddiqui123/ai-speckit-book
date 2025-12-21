# backend/core/config.py
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    DATABASE_URL: str = "sqlite:///./dev.db"
    SECRET_KEY: str = "dev-secret-key"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    OPENROUTER_API_KEY: str = "dev-openrouter-key"
    QDRANT_URL: str = "http://localhost:6333"
    QDRANT_API_KEY: str = "dev-qdrant-key"
    CLIENT_ORIGIN_URL: str = "http://localhost:3000"
    EMBEDDING_MODEL: str = "openai/text-embedding-3-small"  # Use a known 1536-dim model for consistency
    CHAT_MODEL: str = "google/gemini-flash-1.5"


@lru_cache()
def get_settings():
    return Settings()
