import json
from decimal import Decimal

import redis

from app.catalog_client import CatalogClientError, fetch_product, product_to_cart_fields
from app.config import get_settings
from app.exceptions import OutOfStockException, ProductNotFoundException
from app.schemas.cart import CartDTO, CartItemDTO

CART_CACHE_KEY_PREFIX = "storium:cache:cart:"


def _cart_key(cart_id: str) -> str:
    return f"{CART_CACHE_KEY_PREFIX}{cart_id}"


def _cart_ttl_seconds() -> int:
    return max(0, int(get_settings().cart_cache_ttl_seconds))


def _refresh_cart_ttl(r: redis.Redis, cart_id: str) -> None:
    ttl = _cart_ttl_seconds()
    if ttl > 0:
        r.expire(_cart_key(cart_id), ttl)


def _load_raw(r: redis.Redis, cart_id: str) -> dict:
    raw = r.get(_cart_key(cart_id))
    if not raw:
        return {}
    data = json.loads(raw)
    _refresh_cart_ttl(r, cart_id)
    return data


def _save_raw(r: redis.Redis, cart_id: str, data: dict) -> None:
    key = _cart_key(cart_id)
    ttl = _cart_ttl_seconds()
    if not data:
        r.delete(key)
        return
    payload = json.dumps(data)
    if ttl > 0:
        r.setex(key, ttl, payload)
    else:
        r.set(key, payload)


def get_cart(r: redis.Redis, cart_id: str) -> CartDTO:
    raw = _load_raw(r, cart_id)
    items: list[CartItemDTO] = []
    for item in raw.values():
        items.append(
            CartItemDTO(
                product_id=item["product_id"],
                name=item["name"],
                price=Decimal(item["price"]),
                quantity=item["quantity"],
                image_url=item.get("image_url"),
            ),
        )
    total = sum(i.price * i.quantity for i in items)
    return CartDTO(
        items=items,
        total_price=total,
        item_count=sum(i.quantity for i in items),
        unique_item_count=len(items),
    )


def add_item(r: redis.Redis, cart_id: str, product_id: int, quantity: int = 1) -> CartDTO:
    try:
        pdata = fetch_product(product_id)
    except CatalogClientError as e:
        raise ProductNotFoundException(str(e)) from e
    name, price, stock, is_active, image_url = product_to_cart_fields(pdata)
    if not pdata or not is_active:
        raise ProductNotFoundException(f"Ürün bulunamadı: id={product_id}")

    cart = _load_raw(r, cart_id)
    key = str(product_id)
    current_qty = cart.get(key, {}).get("quantity", 0)
    new_qty = current_qty + quantity

    if stock < new_qty:
        raise OutOfStockException(name, stock)

    cart[key] = {
        "product_id": product_id,
        "name": name,
        "price": str(price),
        "quantity": new_qty,
        "image_url": image_url,
    }
    _save_raw(r, cart_id, cart)
    return get_cart(r, cart_id)


def update_item(
    r: redis.Redis,
    cart_id: str,
    product_id: int,
    quantity: int,
) -> CartDTO:
    if quantity <= 0:
        return remove_item(r, cart_id, product_id)

    try:
        pdata = fetch_product(product_id)
    except CatalogClientError as e:
        raise ProductNotFoundException(str(e)) from e
    name, price, stock, is_active, image_url = product_to_cart_fields(pdata)
    if not pdata or not is_active:
        raise ProductNotFoundException(f"Ürün bulunamadı: id={product_id}")
    if stock < quantity:
        raise OutOfStockException(name, stock)

    cart = _load_raw(r, cart_id)
    key = str(product_id)
    if key in cart:
        cart[key]["quantity"] = quantity
        cart[key]["name"] = name
        cart[key]["price"] = str(price)
        cart[key]["image_url"] = image_url
        _save_raw(r, cart_id, cart)
    return get_cart(r, cart_id)


def remove_item(r: redis.Redis, cart_id: str, product_id: int) -> CartDTO:
    cart = _load_raw(r, cart_id)
    cart.pop(str(product_id), None)
    _save_raw(r, cart_id, cart)
    return get_cart(r, cart_id)


def clear_cart(r: redis.Redis, cart_id: str) -> None:
    r.delete(_cart_key(cart_id))
