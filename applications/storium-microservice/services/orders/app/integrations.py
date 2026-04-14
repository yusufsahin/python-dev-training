import json
from decimal import Decimal
from typing import Any

import httpx

from app.config import get_settings
from app.exceptions import IntegrationError


def _headers_internal() -> dict[str, str]:
    return {"X-Internal-Token": get_settings().internal_api_token}


def catalog_decrement_batch(items: list[dict[str, int]]) -> None:
    s = get_settings()
    url = f"{s.catalog_service_url.rstrip('/')}/internal/stock/decrement-batch"
    try:
        r = httpx.post(url, json={"items": items}, headers=_headers_internal(), timeout=30.0)
    except httpx.RequestError as e:
        raise IntegrationError(f"Catalog stok düşürme başarısız: {e}") from e
    if r.status_code >= 400:
        raise IntegrationError(r.text or f"Catalog HTTP {r.status_code}")


def catalog_increment_batch(items: list[dict[str, int]]) -> None:
    s = get_settings()
    url = f"{s.catalog_service_url.rstrip('/')}/internal/stock/increment-batch"
    try:
        r = httpx.post(url, json={"items": items}, headers=_headers_internal(), timeout=30.0)
    except httpx.RequestError as e:
        raise IntegrationError(f"Catalog stok iade başarısız: {e}") from e
    if r.status_code >= 400:
        raise IntegrationError(r.text or f"Catalog HTTP {r.status_code}")


def cart_fetch_json(cart_id: str) -> dict[str, Any]:
    s = get_settings()
    url = f"{s.cart_service_url.rstrip('/')}/api/cart"
    try:
        r = httpx.get(url, headers={"X-Cart-Id": cart_id}, timeout=15.0)
    except httpx.RequestError as e:
        raise IntegrationError(f"Sepet okunamadı: {e}") from e
    if r.status_code >= 400:
        raise IntegrationError(r.text or f"Cart HTTP {r.status_code}")
    return json.loads(r.text)


def cart_clear(cart_id: str) -> None:
    s = get_settings()
    url = f"{s.cart_service_url.rstrip('/')}/api/cart"
    try:
        r = httpx.delete(url, headers={"X-Cart-Id": cart_id}, timeout=15.0)
    except httpx.RequestError as e:
        raise IntegrationError(f"Sepet temizlenemedi: {e}") from e
    if r.status_code >= 400:
        raise IntegrationError(r.text or f"Cart HTTP {r.status_code}")


def parse_cart_dto(data: dict[str, Any]) -> tuple[list[tuple[int, int, str, Decimal]], Decimal]:
    """(product_id, quantity, name, unit_price) listesi ve total."""
    from app.schemas.cart import CartDTO

    dto = CartDTO.model_validate(data)
    lines: list[tuple[int, int, str, Decimal]] = []
    for it in dto.items:
        lines.append((it.product_id, it.quantity, it.name, it.price))
    return lines, dto.total_price
