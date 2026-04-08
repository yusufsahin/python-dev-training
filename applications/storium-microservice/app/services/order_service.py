from sqlalchemy.orm import Session

from app.exceptions import (
    EmptyCartException,
    InvalidOrderStatusTransitionException,
    OrderAccessDeniedException,
    OrderNotFoundException,
    OutOfStockException,
)
from app.order_status import status_display
from app.repositories import catalog_repo, order_repo
from app.schemas.cart import CartDTO
from app.schemas.order import CheckoutInputDTO, OrderItemOutputDTO, OrderOutputDTO
from app.services.notifications import EmailNotificationService


class OrderService:
    VALID_TRANSITIONS = {
        "pending": ["confirmed", "cancelled"],
        "confirmed": ["shipped", "cancelled"],
        "shipped": ["delivered"],
        "delivered": [],
        "cancelled": [],
    }

    def __init__(self, db: Session):
        self._db = db
        self._notify = EmailNotificationService(db)

    def create_order(
        self,
        user_id: int,
        cart_dto: CartDTO,
        checkout_input: CheckoutInputDTO,
    ) -> OrderOutputDTO:
        if not cart_dto.items:
            raise EmptyCartException("Sepet boş, sipariş oluşturulamaz.")

        for item in cart_dto.items:
            product = catalog_repo.product_get_by_id(self._db, item.product_id)
            if not product or product.stock < item.quantity:
                raise OutOfStockException(
                    item.name,
                    product.stock if product else 0,
                )

        order_data = {
            "user_id": user_id,
            "status": "pending",
            "total_price": cart_dto.total_price,
            "shipping_name": checkout_input.shipping_name,
            "shipping_address": checkout_input.shipping_address,
            "shipping_city": checkout_input.shipping_city,
            "shipping_phone": checkout_input.shipping_phone,
            "notes": checkout_input.notes,
            "items": [
                {
                    "product_id": item.product_id,
                    "product_name": item.name,
                    "unit_price": item.price,
                    "quantity": item.quantity,
                }
                for item in cart_dto.items
            ],
        }

        try:
            order = order_repo.order_create(self._db, **order_data)
            for item in cart_dto.items:
                catalog_repo.product_decrement_stock(self._db, item.product_id, item.quantity)
            self._db.commit()
        except Exception:
            self._db.rollback()
            raise

        order_dto = self._order_to_dto(order)
        self._notify.send_order_placed(order_dto)
        return order_dto

    def get_user_orders(self, user_id: int) -> list[OrderOutputDTO]:
        orders = order_repo.order_get_user_orders(self._db, user_id)
        return [self._order_to_dto(o) for o in orders]

    def get_order_detail(self, order_id: int, user_id: int) -> OrderOutputDTO:
        order = order_repo.order_get_by_id(self._db, order_id)
        if not order:
            raise OrderNotFoundException(f"Sipariş bulunamadı: id={order_id}")
        if order.user_id != user_id:
            raise OrderAccessDeniedException("Bu siparişe erişim yetkiniz yok.")
        return self._order_to_dto(order)

    def update_order_status(self, order_id: int, new_status: str) -> OrderOutputDTO:
        order = order_repo.order_get_by_id(self._db, order_id)
        if not order:
            raise OrderNotFoundException(f"Sipariş bulunamadı: id={order_id}")

        allowed = self.VALID_TRANSITIONS.get(order.status, [])
        if new_status not in allowed:
            raise InvalidOrderStatusTransitionException(order.status, new_status)

        try:
            updated = order_repo.order_update_status(self._db, order_id, new_status)
            self._db.commit()
        except Exception:
            self._db.rollback()
            raise

        assert updated is not None
        order_dto = self._order_to_dto(updated)
        self._notify.send_order_status_changed(order_dto)
        return order_dto

    def _order_to_dto(self, order) -> OrderOutputDTO:
        return OrderOutputDTO(
            id=order.id,
            status=order.status,
            status_display=status_display(order.status),
            total_price=order.total_price,
            shipping_name=order.shipping_name,
            shipping_address=order.shipping_address,
            shipping_city=order.shipping_city,
            shipping_phone=order.shipping_phone or "",
            notes=order.notes or "",
            items=[self._order_item_to_dto(i) for i in order.items],
            created_at=order.created_at.isoformat(),
            updated_at=order.updated_at.isoformat(),
        )

    def _order_item_to_dto(self, item) -> OrderItemOutputDTO:
        return OrderItemOutputDTO(
            product_id=item.product_id,
            product_name=item.product_name,
            unit_price=item.unit_price,
            quantity=item.quantity,
            line_total=item.line_total,
        )
