from typing import Annotated, Optional

import redis
from fastapi import Depends, Header, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.config import get_settings
from app.database import get_db
from app.repositories import user_repo
from app.security import decode_token
from app.models import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login", auto_error=False)


def get_redis() -> redis.Redis:
    settings = get_settings()
    return redis.Redis.from_url(settings.redis_url, decode_responses=True)


def get_cart_id(x_cart_id: Annotated[Optional[str], Header(alias="X-Cart-Id")] = None) -> str:
    if x_cart_id and x_cart_id.strip():
        return x_cart_id.strip()
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="X-Cart-Id başlığı gerekli (istemci UUID üretir).",
    )


def get_current_user_optional(
    token: Annotated[Optional[str], Depends(oauth2_scheme)],
    db: Session = Depends(get_db),
) -> Optional[User]:
    if not token:
        return None
    try:
        payload = decode_token(token)
        uid = int(payload.get("sub", 0))
    except (ValueError, TypeError):
        return None
    return user_repo.user_get_by_id(db, uid)


def get_current_user(
    user: Annotated[Optional[User], Depends(get_current_user_optional)],
) -> User:
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Oturum gerekli.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user
