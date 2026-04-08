from decimal import Decimal

from django.test import Client, TestCase
from django.urls import reverse

from core.dtos.cart_dtos import CartDTO, CartItemDTO
from modules.catalog.models import Category, Product


class CartDTOTests(TestCase):
    def test_cart_item_line_total_computed(self):
        item = CartItemDTO(
            product_id=1,
            name="X",
            price=Decimal("10.00"),
            quantity=3,
            image_url=None,
        )
        self.assertEqual(item.line_total, Decimal("30.00"))

    def test_cart_dto_aggregates(self):
        cart = CartDTO(
            items=[
                CartItemDTO(
                    product_id=1,
                    name="A",
                    price=Decimal("5.00"),
                    quantity=2,
                    image_url=None,
                ),
            ],
            total_price=Decimal("10.00"),
            item_count=2,
            unique_item_count=1,
        )
        self.assertEqual(cart.items[0].line_total, Decimal("10.00"))
        self.assertEqual(len(cart.items), 1)


class CartViewsTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.category = Category.objects.create(name="Gıda", slug="gida", is_active=True)
        self.product = Product.objects.create(
            category=self.category,
            name="Çay",
            slug="cay",
            price=Decimal("25.00"),
            stock=10,
            is_active=True,
        )

    def test_add_to_cart_sets_session(self):
        url = reverse("cart:cart_add")
        response = self.client.post(
            url,
            {
                "product_id": self.product.id,
                "quantity": 2,
                "next": reverse("cart:cart_detail"),
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertIn("cart", self.client.session)
        cart = self.client.session["cart"]
        self.assertIn(str(self.product.id), cart)
        self.assertEqual(cart[str(self.product.id)]["quantity"], 2)

    def test_cart_detail_shows_items(self):
        self.client.post(
            reverse("cart:cart_add"),
            {
                "product_id": self.product.id,
                "quantity": 1,
                "next": reverse("cart:cart_detail"),
            },
        )
        response = self.client.get(reverse("cart:cart_detail"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Çay")
