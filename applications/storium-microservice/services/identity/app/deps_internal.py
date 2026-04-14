from typing import Annotated, Optional

from fastapi import Header, HTTPException, status

from app.config import get_settings


def verify_internal_token(
    x_internal_token: Annotated[Optional[str], Header(alias="X-Internal-Token")] = None,
) -> None:
    expected = get_settings().internal_api_token
    if not x_internal_token or x_internal_token.strip() != expected:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Geçersiz iç API anahtarı.")
