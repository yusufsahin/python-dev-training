from decimal import Decimal

import httpx

from app.config import get_settings


class CatalogClientError(Exception):
    pass


def fetch_product(product_id: int) -> dict:
    s = get_settings()
    url = f"{s.catalog_service_url.rstrip('/')}/internal/products/{product_id}"
    try:
        r = httpx.get(
            url,
            headers={"X-Internal-Token": s.internal_api_token},
            timeout=15.0,
        )
    except httpx.RequestError as e:
        raise CatalogClientError(f"Catalog erişilemedi: {e}") from e
    if r.status_code == 404:
        return {}
    r.raise_for_status()
    return r.json()


def product_to_cart_fields(data: dict) -> tuple[str, Decimal, int, bool, str | None]:
    if not data:
        return "", Decimal("0"), 0, False, None
    price = data["price"]
    if isinstance(price, str):
        price = Decimal(price)
    return (
        data["name"],
        price,
        int(data["stock"]),
        bool(data.get("is_active", True)),
        data.get("image_url"),
    )
