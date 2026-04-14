from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import User


def user_get_by_email(db: Session, email: str) -> Optional[User]:
    return db.scalar(select(User).where(User.email == email))


def user_get_by_username(db: Session, username: str) -> Optional[User]:
    return db.scalar(select(User).where(User.username == username))


def user_get_by_id(db: Session, user_id: int) -> Optional[User]:
    return db.get(User, user_id)


def user_create(db: Session, *, email: str, username: str, hashed_password: str) -> User:
    u = User(email=email, username=username, hashed_password=hashed_password)
    db.add(u)
    db.flush()
    db.refresh(u)
    return u
