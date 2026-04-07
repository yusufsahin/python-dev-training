from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    mongodb_uri: str = "mongodb://127.0.0.1:27017"
    mongodb_db: str = "tasks"
    task_collection: str = "task_item"

    cors_origins: str = "http://localhost:5173,http://127.0.0.1:5173,http://localhost:3000"


@lru_cache
def get_settings() -> Settings:
    return Settings()
