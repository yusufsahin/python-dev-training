from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    secret_key: str = "change-me-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60 * 24

    database_url: str = "postgresql+psycopg2://storium_user:storium_password@localhost:5432/identity_db"
    internal_api_token: str = "change-me-internal-token"

    cors_origins: str = (
        "http://localhost:3000,http://127.0.0.1:3000,"
        "http://localhost:9080,http://127.0.0.1:9080,"
        "http://localhost:8001,http://127.0.0.1:8001"
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
