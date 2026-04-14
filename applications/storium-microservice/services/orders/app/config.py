from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    database_url: str = "postgresql+psycopg2://storium_user:storium_password@localhost:5432/orders_db"
    secret_key: str = "change-me-in-production"
    algorithm: str = "HS256"

    catalog_service_url: str = "http://localhost:8000"
    cart_service_url: str = "http://localhost:8000"
    internal_api_token: str = "change-me-internal-token"

    rabbitmq_url: str = "amqp://storium:storium_pass@localhost:5672/"
    rabbitmq_exchange: str = "storium.events"
    rabbitmq_routing_key: str = "order.created"
    notifications_queue: str = "storium.notifications"

    cors_origins: str = (
        "http://localhost:3000,http://127.0.0.1:3000,"
        "http://localhost:9080,http://127.0.0.1:9080,"
        "http://localhost:8001,http://127.0.0.1:8001"
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
