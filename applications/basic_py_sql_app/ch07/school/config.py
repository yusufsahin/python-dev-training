import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()


def _postgres_uri() -> str:
    user = os.environ.get("POSTGRES_USER", "postgres")
    password = os.environ.get("POSTGRES_PASSWORD", "postgres")
    host = os.environ.get("POSTGRES_HOST", "localhost")
    port = os.environ.get("POSTGRES_PORT", "5432")
    db_name = os.environ.get("POSTGRES_DB", "school")
    return f"postgresql+psycopg://{user}:{password}@{host}:{port}/{db_name}"


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "ch07-dev-only-change-in-production")
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or _postgres_uri()
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_TIME_LIMIT = None


def static_dir() -> Path:
    return Path(__file__).resolve().parent / "static"
