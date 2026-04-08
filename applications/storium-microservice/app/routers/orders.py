import redis
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.database import get_db
from app.deps import get_cart_id, get_current_user, get_redis
from app.exceptions import (
    EmptyCartException,
    InvalidOrderStatusTransitionException,
    OrderAccessDeniedException,
    OrderNotFoundException,
    OutOfStockException,
    StoriumBaseException,
)
from app.models import User
from app.schemas.order import CheckoutInputDTO, OrderOutputDTO
from app.services import cart_service
from app.services.order_service import OrderService


class OrderStatusBody(BaseModel):
    status: str = Field(min_length=1, max_length=20)

router = APIRouter(prefix="/orders", tags=["orders"])


def _map_order_error(e: StoriumBaseException) -> HTTPException:
    if isinstance(e, OrderNotFoundException):
        return HTTPException(status_code=404, detail=str(e))
    if isinstance(e, OrderAccessDeniedException):
        return HTTPException(status_code=403, detail=str(e))
    if isinstance(e, (EmptyCartException, OutOfStockException)):
        return HTTPException(status_code=400, detail=str(e))
    if isinstance(e, InvalidOrderStatusTransitionException):
        return HTTPException(status_code=400, detail=str(e))
    return HTTPException(status_code=400, detail=str(e))


@router.post("/checkout", response_model=OrderOutputDTO)
def checkout(
    body: CheckoutInputDTO,
    db: Session = Depends(get_db),
    r: redis.Redis = Depends(get_redis),
    cart_id: str = Depends(get_cart_id),
    user: User = Depends(get_current_user),
) -> OrderOutputDTO:
    cart = cart_service.get_cart(r, cart_id)
    svc = OrderService(db)
    try:
        order = svc.create_order(user.id, cart, body)
    except StoriumBaseException as e:
        raise _map_order_error(e) from e
    cart_service.clear_cart(r, cart_id)
    return order


@router.get("", response_model=list[OrderOutputDTO])
def list_orders(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> list[OrderOutputDTO]:
    return OrderService(db).get_user_orders(user.id)


@router.get("/{order_id}", response_model=OrderOutputDTO)
def order_detail(
    order_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> OrderOutputDTO:
    try:
        return OrderService(db).get_order_detail(order_id, user.id)
    except StoriumBaseException as e:
        raise _map_order_error(e) from e


@router.patch("/{order_id}/status", response_model=OrderOutputDTO)
def update_status(
    order_id: int,
    body: OrderStatusBody,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> OrderOutputDTO:
    # Basit MVP: oturum açmış her kullanıcı (ileride admin rolü)
    try:
        return OrderService(db).update_order_status(order_id, body.status)
    except StoriumBaseException as e:
        raise _map_order_error(e) from e
