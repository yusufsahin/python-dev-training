import os
from pathlib import Path

from dotenv import load_dotenv
from flask import Flask

load_dotenv()


def _postgres_uri() -> str:
    user = os.environ.get("POSTGRES_USER", "postgres")
    password = os.environ.get("POSTGRES_PASSWORD", "postgres")
    host = os.environ.get("POSTGRES_HOST", "localhost")
    port = os.environ.get("POSTGRES_PORT", "5432")
    db_name = os.environ.get("POSTGRES_DB", "tasks")
    return f"postgresql+psycopg://{user}:{password}@{host}:{port}/{db_name}"


def resolve_database_uri(app: Flask) -> str:
    """DATABASE_URL → Postgres/SQLite URL; yoksa POSTGRES_HOST → Postgres; aksi halde instance/tasks.db."""
    if url := os.environ.get("DATABASE_URL"):
        return url
    if os.environ.get("POSTGRES_HOST"):
        return _postgres_uri()
    Path(app.instance_path).mkdir(parents=True, exist_ok=True)
    p = Path(app.instance_path) / "tasks.db"
    return f"sqlite:///{p.as_posix()}"


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "ch09-dev-only-change-in-production")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_TIME_LIMIT = None
