from decimal import Decimal

from django.contrib.auth.models import User
from django.test import TestCase

from apps.notifications.services import EmailNotificationService
from core.dtos.order_dtos import OrderItemOutputDTO, OrderOutputDTO


class EmailNotificationServiceTests(TestCase):
    def test_send_order_placed_noop_when_order_missing(self):
        order = OrderOutputDTO(
            id=999_999,
            status="pending",
            status_display="Beklemede",
            total_price=Decimal("10.00"),
            shipping_name="A",
            shipping_address="B",
            shipping_city="C",
            shipping_phone="",
            notes="",
            items=[],
            created_at="",
            updated_at="",
        )
        EmailNotificationService().send_order_placed(order)

    def test_send_order_placed_with_order_and_user(self):
        user = User.objects.create_user(
            username="buyer",
            password="x",
            email="buyer@example.com",
        )
        from apps.orders.models import Order, OrderItem
        from apps.catalog.models import Category, Product

        cat = Category.objects.create(name="C", slug="c", is_active=True)
        p = Product.objects.create(
            category=cat,
            name="P",
            slug="p",
            price=Decimal("5.00"),
            stock=1,
            is_active=True,
        )
        order = Order.objects.create(
            user=user,
            total_price=Decimal("5.00"),
            shipping_name="A",
            shipping_address="B",
            shipping_city="C",
        )
        OrderItem.objects.create(
            order=order,
            product=p,
            product_name="P",
            unit_price=Decimal("5.00"),
            quantity=1,
        )
        dto = OrderOutputDTO(
            id=order.id,
            status=order.status,
            status_display=order.get_status_display(),
            total_price=order.total_price,
            shipping_name=order.shipping_name,
            shipping_address=order.shipping_address,
            shipping_city=order.shipping_city,
            shipping_phone=order.shipping_phone,
            notes=order.notes or "",
            items=[
                OrderItemOutputDTO(
                    product_id=p.id,
                    product_name="P",
                    unit_price=Decimal("5.00"),
                    quantity=1,
                    line_total=Decimal("5.00"),
                ),
            ],
            created_at=order.created_at.isoformat(),
            updated_at=order.updated_at.isoformat(),
        )
        EmailNotificationService().send_order_placed(dto)
