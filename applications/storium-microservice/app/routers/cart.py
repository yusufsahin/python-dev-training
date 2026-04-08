from fastapi import APIRouter, Depends, HTTPException, Query
import redis
from sqlalchemy.orm import Session

from app.database import get_db
from app.deps import get_cart_id, get_redis
from app.exceptions import OutOfStockException, ProductNotFoundException, StoriumBaseException
from app.schemas.cart import CartDTO, CartItemAdd
from app.services import cart_service

router = APIRouter(prefix="/cart", tags=["cart"])


def _handle_domain(exc: StoriumBaseException) -> HTTPException:
    if isinstance(exc, ProductNotFoundException):
        return HTTPException(status_code=404, detail=str(exc))
    if isinstance(exc, OutOfStockException):
        return HTTPException(status_code=400, detail=str(exc))
    return HTTPException(status_code=400, detail=str(exc))


@router.get("", response_model=CartDTO)
def get_cart(
    cart_id: str = Depends(get_cart_id),
    r: redis.Redis = Depends(get_redis),
) -> CartDTO:
    return cart_service.get_cart(r, cart_id)


@router.post("/items", response_model=CartDTO)
def add_item(
    body: CartItemAdd,
    db: Session = Depends(get_db),
    r: redis.Redis = Depends(get_redis),
    cart_id: str = Depends(get_cart_id),
) -> CartDTO:
    try:
        return cart_service.add_item(db, r, cart_id, body.product_id, body.quantity)
    except StoriumBaseException as e:
        raise _handle_domain(e) from e


@router.patch("/items/{product_id}", response_model=CartDTO)
def update_item(
    product_id: int,
    quantity: int = Query(..., ge=0),
    db: Session = Depends(get_db),
    r: redis.Redis = Depends(get_redis),
    cart_id: str = Depends(get_cart_id),
) -> CartDTO:
    try:
        return cart_service.update_item(db, r, cart_id, product_id, quantity)
    except StoriumBaseException as e:
        raise _handle_domain(e) from e


@router.delete("/items/{product_id}", response_model=CartDTO)
def remove_item(
    product_id: int,
    r: redis.Redis = Depends(get_redis),
    cart_id: str = Depends(get_cart_id),
) -> CartDTO:
    return cart_service.remove_item(r, cart_id, product_id)


@router.delete("")
def clear_cart(
    r: redis.Redis = Depends(get_redis),
    cart_id: str = Depends(get_cart_id),
) -> dict:
    cart_service.clear_cart(r, cart_id)
    return {"ok": True}
