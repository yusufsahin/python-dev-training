from typing import Annotated

from fastapi import APIRouter, Depends, Header, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.deps import CurrentUserId
from app.exceptions import (
    EmptyCartException,
    IntegrationError,
    OrderNotFoundException,
    StoriumBaseException,
)
from app.models import Order
from app.order_status import status_display
from app.schemas.order import CheckoutInputDTO, OrderItemOutputDTO, OrderOutputDTO
from app.services.order_service import OrderService

router = APIRouter(prefix="/orders", tags=["orders"])


def _to_order_out(o: Order) -> OrderOutputDTO:
    items = [
        OrderItemOutputDTO(
            product_id=it.product_id,
            product_name=it.product_name,
            unit_price=it.unit_price,
            quantity=it.quantity,
            line_total=it.unit_price * it.quantity,
        )
        for it in o.items
    ]
    return OrderOutputDTO(
        id=o.id,
        status=o.status,
        status_display=status_display(o.status),
        total_price=o.total_price,
        shipping_name=o.shipping_name,
        shipping_address=o.shipping_address,
        shipping_city=o.shipping_city,
        shipping_phone=o.shipping_phone,
        notes=o.notes,
        items=items,
        created_at=o.created_at.isoformat(),
        updated_at=o.updated_at.isoformat(),
    )


def _domain_http(exc: StoriumBaseException) -> HTTPException:
    if isinstance(exc, OrderNotFoundException):
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sipariş bulunamadı.")
    if isinstance(exc, EmptyCartException):
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc) or "Sepet boş.")
    if isinstance(exc, IntegrationError):
        return HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail=str(exc))
    return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))


@router.get("", response_model=list[OrderOutputDTO])
def list_orders(
    user_id: CurrentUserId,
    db: Session = Depends(get_db),
) -> list[OrderOutputDTO]:
    svc = OrderService(db)
    orders = svc.list_orders(user_id)
    return [_to_order_out(o) for o in orders]


@router.get("/{order_id}", response_model=OrderOutputDTO)
def get_order(
    order_id: int,
    user_id: CurrentUserId,
    db: Session = Depends(get_db),
) -> OrderOutputDTO:
    svc = OrderService(db)
    try:
        o = svc.get_order(user_id, order_id)
    except OrderNotFoundException as e:
        raise _domain_http(e) from e
    return _to_order_out(o)


@router.post("/checkout", response_model=OrderOutputDTO)
def checkout(
    body: CheckoutInputDTO,
    user_id: CurrentUserId,
    db: Session = Depends(get_db),
    x_cart_id: Annotated[str | None, Header(alias="X-Cart-Id")] = None,
) -> OrderOutputDTO:
    if not x_cart_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="X-Cart-Id başlığı gerekli.",
        )
    svc = OrderService(db)
    try:
        o = svc.checkout(user_id, x_cart_id, body)
    except StoriumBaseException as e:
        raise _domain_http(e) from e
    return _to_order_out(o)
