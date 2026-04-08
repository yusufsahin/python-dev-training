from decimal import Decimal

from django.contrib.auth.models import User
from django.http import QueryDict
from django.test import Client, TestCase
from django.urls import reverse
from pydantic import ValidationError

from core.dtos.order_dtos import CheckoutInputDTO, checkout_validation_messages
from modules.catalog.models import Category, Product


class CheckoutInputDTOTests(TestCase):
    def test_from_post_valid(self):
        dto = CheckoutInputDTO.from_post(
            {
                "shipping_name": "Ali Veli",
                "shipping_address": "Adres 1",
                "shipping_city": "Ankara",
                "shipping_phone": "555",
                "notes": "Kapıcıya bırakın",
            }
        )
        self.assertEqual(dto.shipping_name, "Ali Veli")
        self.assertEqual(dto.shipping_phone, "555")
        self.assertEqual(dto.notes, "Kapıcıya bırakın")

    def test_from_post_strips_whitespace(self):
        dto = CheckoutInputDTO.from_post(
            {
                "shipping_name": "  Ali  ",
                "shipping_address": " Sokak ",
                "shipping_city": "İzmir",
            }
        )
        self.assertEqual(dto.shipping_name, "Ali")
        self.assertEqual(dto.shipping_address, "Sokak")

    def test_from_post_querydict(self):
        qd = QueryDict(mutable=True)
        qd.update(
            {
                "shipping_name": "A",
                "shipping_address": "B",
                "shipping_city": "C",
            }
        )
        dto = CheckoutInputDTO.from_post(qd)
        self.assertEqual(dto.shipping_name, "A")

    def test_empty_name_validation_messages(self):
        with self.assertRaises(ValidationError) as ctx:
            CheckoutInputDTO.from_post(
                {
                    "shipping_name": "",
                    "shipping_address": "X",
                    "shipping_city": "Y",
                }
            )
        msgs = checkout_validation_messages(ctx.exception)
        self.assertIn("Ad Soyad zorunludur.", msgs)

    def test_empty_address_and_city_messages(self):
        with self.assertRaises(ValidationError) as ctx:
            CheckoutInputDTO.from_post(
                {
                    "shipping_name": "A",
                    "shipping_address": "",
                    "shipping_city": "",
                }
            )
        msgs = checkout_validation_messages(ctx.exception)
        self.assertIn("Adres zorunludur.", msgs)
        self.assertIn("Şehir zorunludur.", msgs)


class OrdersAuthTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_checkout_redirects_when_not_logged_in(self):
        response = self.client.get(reverse("orders:checkout"))
        self.assertEqual(response.status_code, 302)
        self.assertIn("/giris/", response.url)


class OrdersCheckoutFlowTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="ali", password="testpass123")
        self.category = Category.objects.create(name="Kitap", slug="kitap", is_active=True)
        self.product = Product.objects.create(
            category=self.category,
            name="Roman",
            slug="roman",
            price=Decimal("40.00"),
            stock=5,
            is_active=True,
        )

    def test_checkout_creates_order_and_clears_cart(self):
        self.client.login(username="ali", password="testpass123")
        self.client.post(
            reverse("cart:cart_add"),
            {
                "product_id": self.product.id,
                "quantity": 1,
                "next": reverse("cart:cart_detail"),
            },
        )
        response = self.client.post(
            reverse("orders:checkout"),
            {
                "shipping_name": "Ali Veli",
                "shipping_address": "Mahalle 1",
                "shipping_city": "İstanbul",
                "shipping_phone": "",
                "notes": "",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertIn("/siparis/tamamlandi/", response.url)
        self.assertEqual(self.client.session.get("cart", {}), {})
        self.assertTrue(self.user.orders.exists())
        order = self.user.orders.first()
        self.assertEqual(order.items.count(), 1)
        self.product.refresh_from_db()
        self.assertEqual(self.product.stock, 4)
