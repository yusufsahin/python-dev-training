from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    secret_key: str = "change-me-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60 * 24

    database_url: str = "postgresql+psycopg2://storium_user:storium_password@localhost:5432/storium_db"

    redis_url: str = "redis://localhost:6379/1"

    # Sepet verisi Redis önbelleğinde (JSON). 0 = süresiz (SET); >0 = saniye cinsinden TTL (SETEX + her okumada EXPIRE yenileme).
    cart_cache_ttl_seconds: int = 60 * 60 * 24 * 30

    cors_origins: str = (
        "http://localhost:3000,http://127.0.0.1:3000,"
        "http://localhost:9080,http://127.0.0.1:9080,"
        "http://localhost:8001,http://127.0.0.1:8001"
    )

    default_from_email: str = "noreply@storium.local"
    smtp_host: str = ""
    smtp_port: int = 587
    smtp_user: str = ""
    smtp_password: str = ""


@lru_cache
def get_settings() -> Settings:
    return Settings()
