from typing import Any

from fastapi import HTTPException, status
from jose import JWTError, jwt

from app.config import get_settings


def decode_access_token(token: str) -> dict[str, Any]:
    s = get_settings()
    try:
        return jwt.decode(token, s.secret_key, algorithms=[s.algorithm])
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Geçersiz veya süresi dolmuş oturum",
        ) from None
