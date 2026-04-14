import logging
from decimal import Decimal

from sqlalchemy.orm import Session

from app.exceptions import EmptyCartException, IntegrationError, OrderNotFoundException
from app.integrations import (
    cart_clear,
    cart_fetch_json,
    catalog_decrement_batch,
    catalog_increment_batch,
    parse_cart_dto,
)
from app.models import Order
from app.publisher import publish_order_created
from app.repositories import order_repo
from app.schemas.order import CheckoutInputDTO

logger = logging.getLogger(__name__)


class OrderService:
    def __init__(self, db: Session) -> None:
        self._db = db

    def list_orders(self, user_id: int) -> list[Order]:
        return order_repo.order_get_user_orders(self._db, user_id)

    def get_order(self, user_id: int, order_id: int) -> Order:
        o = order_repo.order_get_by_id_for_user(self._db, order_id, user_id)
        if o is None:
            raise OrderNotFoundException()
        return o

    def checkout(self, user_id: int, cart_id: str, shipping: CheckoutInputDTO) -> Order:
        if not cart_id or not cart_id.strip():
            raise EmptyCartException()

        try:
            raw = cart_fetch_json(cart_id)
        except IntegrationError:
            raise

        lines, cart_total = parse_cart_dto(raw)
        if not lines:
            raise EmptyCartException()

        stock_items = [{"product_id": pid, "quantity": qty} for pid, qty, _, _ in lines]

        try:
            catalog_decrement_batch(stock_items)
        except IntegrationError as e:
            raise EmptyCartException(str(e)) from e

        item_rows = [
            {
                "product_id": pid,
                "product_name": name,
                "unit_price": price,
                "quantity": qty,
            }
            for pid, qty, name, price in lines
        ]

        try:
            order = order_repo.order_create(
                self._db,
                user_id=user_id,
                status="pending",
                total_price=cart_total,
                shipping_name=shipping.shipping_name,
                shipping_address=shipping.shipping_address,
                shipping_city=shipping.shipping_city,
                shipping_phone=shipping.shipping_phone,
                notes=shipping.notes,
                items=item_rows,
            )
            self._db.commit()
        except Exception:
            self._db.rollback()
            try:
                catalog_increment_batch(stock_items)
            except IntegrationError:
                logger.exception("Order persist failed; stock compensation failed")
            raise

        try:
            cart_clear(cart_id)
        except IntegrationError as e:
            logger.warning("Order saved but cart clear failed: %s", e)

        try:
            publish_order_created(
                {
                    "event": "order.created",
                    "order_id": order.id,
                    "user_id": user_id,
                    "total": str(order.total_price),
                    "items": [
                        {
                            "product_id": it.product_id,
                            "product_name": it.product_name,
                            "quantity": it.quantity,
                        }
                        for it in order.items
                    ],
                }
            )
        except Exception:
            logger.exception("Failed to publish order event (order persisted)")

        return order
