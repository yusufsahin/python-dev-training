from django.db import transaction

from core.dtos.cart_dtos import CartDTO
from core.dtos.order_dtos import CheckoutInputDTO, OrderItemOutputDTO, OrderOutputDTO
from core.exceptions.domain_exceptions import (
    EmptyCartException,
    InvalidOrderStatusTransitionException,
    OrderAccessDeniedException,
    OrderNotFoundException,
    OutOfStockException,
)
from core.repositories.protocols import OrderRepositoryProtocol, ProductRepositoryProtocol


class OrderService:
    VALID_TRANSITIONS = {
        "pending": ["confirmed", "cancelled"],
        "confirmed": ["shipped", "cancelled"],
        "shipped": ["delivered"],
        "delivered": [],
        "cancelled": [],
    }

    def __init__(
        self,
        order_repo: OrderRepositoryProtocol,
        product_repo: ProductRepositoryProtocol,
        notification_service,
    ):
        self.order_repo = order_repo
        self.product_repo = product_repo
        self.notification_service = notification_service

    @transaction.atomic
    def create_order(
        self,
        user_id: int,
        cart_dto: CartDTO,
        checkout_input: CheckoutInputDTO,
    ) -> OrderOutputDTO:
        if not cart_dto.items:
            raise EmptyCartException("Sepet boş, sipariş oluşturulamaz.")

        for item in cart_dto.items:
            product = self.product_repo.get_by_id(item.product_id)
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

        order = self.order_repo.create_order(order_data)

        for item in cart_dto.items:
            self.product_repo.decrement_stock(item.product_id, item.quantity)

        order_dto = self._order_to_dto(order)
        self.notification_service.send_order_placed(order_dto)

        return order_dto

    def get_user_orders(self, user_id: int) -> list[OrderOutputDTO]:
        orders = self.order_repo.get_user_orders(user_id)
        return [self._order_to_dto(o) for o in orders]

    def get_order_detail(self, order_id: int, user_id: int) -> OrderOutputDTO:
        order = self.order_repo.get_by_id(order_id)
        if not order:
            raise OrderNotFoundException(f"Sipariş bulunamadı: id={order_id}")
        if order.user_id != user_id:
            raise OrderAccessDeniedException("Bu siparişe erişim yetkiniz yok.")
        return self._order_to_dto(order)

    def update_order_status(self, order_id: int, new_status: str) -> OrderOutputDTO:
        order = self.order_repo.get_by_id(order_id)
        if not order:
            raise OrderNotFoundException(f"Sipariş bulunamadı: id={order_id}")

        allowed = self.VALID_TRANSITIONS.get(order.status, [])
        if new_status not in allowed:
            raise InvalidOrderStatusTransitionException(order.status, new_status)

        updated_order = self.order_repo.update_status(order_id, new_status)
        order_dto = self._order_to_dto(updated_order)
        self.notification_service.send_order_status_changed(order_dto)
        return order_dto

    def _order_to_dto(self, order) -> OrderOutputDTO:
        return OrderOutputDTO(
            id=order.id,
            status=order.status,
            status_display=order.get_status_display(),
            total_price=order.total_price,
            shipping_name=order.shipping_name,
            shipping_address=order.shipping_address,
            shipping_city=order.shipping_city,
            shipping_phone=order.shipping_phone,
            notes=order.notes or "",
            items=[self._order_item_to_dto(i) for i in order.items.all()],
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
