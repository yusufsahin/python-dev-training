from decimal import Decimal

from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse

from apps.catalog.models import Category, Product
from apps.catalog.service_provider import get_catalog_service


class CatalogServiceNavTests(TestCase):
    def setUp(self):
        self.root = Category.objects.create(name="Kök", slug="kok", is_active=True)
        Category.objects.create(name="Alt", slug="alt", is_active=True, parent=self.root)

    def test_get_category_nav_tree_two_levels(self):
        tree = get_catalog_service().get_category_nav_tree()
        self.assertEqual(len(tree), 1)
        self.assertEqual(tree[0].slug, "kok")
        self.assertEqual(len(tree[0].children), 1)
        self.assertEqual(tree[0].children[0].slug, "alt")


class CatalogViewsTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.category = Category.objects.create(
            name="Elektronik",
            slug="elektronik",
            is_active=True,
        )
        self.product = Product.objects.create(
            category=self.category,
            name="Kulaklık",
            slug="kulaklik",
            description="Test",
            price=Decimal("99.90"),
            stock=3,
            is_active=True,
        )

    def test_home_returns_200(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_category_page_returns_200(self):
        response = self.client.get("/kategori/elektronik/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Elektronik")

    def test_product_detail_returns_200(self):
        response = self.client.get("/urun/kulaklik/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Kulaklık")

    def test_unknown_category_returns_404(self):
        response = self.client.get("/kategori/yok-boyle/")
        self.assertEqual(response.status_code, 404)

    def test_unknown_product_returns_404(self):
        response = self.client.get("/urun/yok/")
        self.assertEqual(response.status_code, 404)

    def test_search_short_query_renders_without_error(self):
        response = self.client.get("/arama/", {"q": "a"})
        self.assertEqual(response.status_code, 200)

    def test_search_finds_product(self):
        response = self.client.get("/arama/", {"q": "Kulak"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Kulaklık")

    def test_inactive_product_not_on_public_detail(self):
        self.product.is_active = False
        self.product.save(update_fields=["is_active"])
        response = self.client.get("/urun/kulaklik/")
        self.assertEqual(response.status_code, 404)


class RegistrationTests(TestCase):
    def test_register_page_returns_200(self):
        response = self.client.get(reverse("register"))
        self.assertEqual(response.status_code, 200)

    def test_register_post_creates_user(self):
        response = self.client.post(
            reverse("register"),
            {
                "username": "yeni_musteri",
                "password1": "Xk9#mPq2$vL8nR!",
                "password2": "Xk9#mPq2$vL8nR!",
            },
        )
        self.assertRedirects(
            response,
            reverse("login"),
            fetch_redirect_response=False,
        )
        self.assertTrue(User.objects.filter(username="yeni_musteri").exists())
