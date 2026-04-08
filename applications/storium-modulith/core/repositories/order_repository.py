from typing import Optional

from django.db.models import QuerySet

from modules.orders.models import Order, OrderItem
from core.repositories.base import BaseRepository


class DjangoOrderRepository(BaseRepository[Order]):
    model_class = Order

    def get_by_id(self, pk: int) -> Optional[Order]:
        return (
            Order.objects.prefetch_related("items__product")
            .filter(pk=pk)
            .first()
        )

    def get_user_orders(self, user_id: int) -> QuerySet[Order]:
        return (
            Order.objects.filter(user_id=user_id)
            .prefetch_related("items")
            .order_by("-created_at")
        )

    def create_order(self, order_data: dict) -> Order:
        items_data = order_data.pop("items")
        order = Order.objects.create(**order_data)
        for item in items_data:
            OrderItem.objects.create(order=order, **item)
        return self.get_by_id(order.pk)  # type: ignore[return-value]

    def update_status(self, order_id: int, status: str) -> Order:
        Order.objects.filter(pk=order_id).update(status=status)
        return Order.objects.prefetch_related("items__product").get(pk=order_id)
