from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    redis_url: str = "redis://localhost:6379/1"
    catalog_service_url: str = "http://localhost:8000"
    internal_api_token: str = "change-me-internal-token"
    cart_cache_ttl_seconds: int = 60 * 60 * 24 * 30

    cors_origins: str = (
        "http://localhost:3000,http://127.0.0.1:3000,"
        "http://localhost:9080,http://127.0.0.1:9080,"
        "http://localhost:8001,http://127.0.0.1:8001"
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
