from typing import Annotated, Optional

import redis
from fastapi import Depends, Header, HTTPException, status

from app.config import get_settings


def get_redis() -> redis.Redis:
    settings = get_settings()
    return redis.Redis.from_url(settings.redis_url, decode_responses=True)


def verify_internal_token(
    x_internal_token: Annotated[Optional[str], Header(alias="X-Internal-Token")] = None,
) -> None:
    expected = get_settings().internal_api_token
    if not x_internal_token or x_internal_token.strip() != expected:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Geçersiz iç API anahtarı.")
