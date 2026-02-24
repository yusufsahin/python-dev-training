"""Engine, SessionLocal, Base ve get_db dependency."""
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.config import settings

engine = create_engine(
    settings.get_engine_url(),
    connect_args={"check_same_thread": False},
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    """Her istekte session aç/kapat (FastAPI dependency)."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
