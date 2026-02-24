"""FastAPI dependencies."""
from collections.abc import Generator

from sqlalchemy.orm import Session

from app.database import SessionLocal


def get_db() -> Generator[Session, None, None]:
    """Veritabanı oturumu (main'deki get_db ile aynı)."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
