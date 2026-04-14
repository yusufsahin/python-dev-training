from typing import Annotated, Optional

import redis
from fastapi import Depends, Header, HTTPException, status

from app.config import get_settings


def get_redis() -> redis.Redis:
    return redis.Redis.from_url(get_settings().redis_url, decode_responses=True)


def get_cart_id(x_cart_id: Annotated[Optional[str], Header(alias="X-Cart-Id")] = None) -> str:
    if x_cart_id and x_cart_id.strip():
        return x_cart_id.strip()
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="X-Cart-Id başlığı gerekli (istemci UUID üretir).",
    )
