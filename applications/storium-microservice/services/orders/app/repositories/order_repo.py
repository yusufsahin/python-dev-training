from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.models import Order, OrderItem


def order_get_by_id(db: Session, pk: int) -> Optional[Order]:
    return db.scalar(
        select(Order)
        .options(selectinload(Order.items))
        .where(Order.id == pk),
    )


def order_get_by_id_for_user(db: Session, order_id: int, user_id: int) -> Optional[Order]:
    o = order_get_by_id(db, order_id)
    if o is None or o.user_id != user_id:
        return None
    return o


def order_get_user_orders(db: Session, user_id: int) -> list[Order]:
    return list(
        db.scalars(
            select(Order)
            .options(selectinload(Order.items))
            .where(Order.user_id == user_id)
            .order_by(Order.created_at.desc()),
        ).all(),
    )


def order_create(
    db: Session,
    *,
    user_id: int,
    status: str,
    total_price,
    shipping_name: str,
    shipping_address: str,
    shipping_city: str,
    shipping_phone: str,
    notes: str,
    items: list[dict],
) -> Order:
    order = Order(
        user_id=user_id,
        status=status,
        total_price=total_price,
        shipping_name=shipping_name,
        shipping_address=shipping_address,
        shipping_city=shipping_city,
        shipping_phone=shipping_phone or "",
        notes=notes or "",
    )
    db.add(order)
    db.flush()
    for row in items:
        db.add(
            OrderItem(
                order_id=order.id,
                product_id=row["product_id"],
                product_name=row["product_name"],
                unit_price=row["unit_price"],
                quantity=row["quantity"],
            ),
        )
    db.flush()
    db.refresh(order)
    return order_get_by_id(db, order.id)  # type: ignore[return-value]


def order_update_status(db: Session, order_id: int, status: str) -> Optional[Order]:
    order = order_get_by_id(db, order_id)
    if order is None:
        return None
    order.status = status
    db.add(order)
    db.flush()
    db.refresh(order)
    return order_get_by_id(db, order_id)
