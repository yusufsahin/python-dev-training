from typing import Optional

from django.db.models import F, Q, QuerySet

from modules.catalog.models import Category, Product
from core.repositories.base import BaseRepository


class DjangoCategoryRepository(BaseRepository[Category]):
    model_class = Category

    def get_by_slug(self, slug: str) -> Optional[Category]:
        return Category.objects.filter(slug=slug, is_active=True).first()

    def get_root_categories(self) -> QuerySet[Category]:
        return Category.objects.filter(parent=None, is_active=True).order_by("name")

    def get_active_children(self, parent_id: int) -> QuerySet[Category]:
        return Category.objects.filter(parent_id=parent_id, is_active=True).order_by("name")


class DjangoProductRepository(BaseRepository[Product]):
    model_class = Product

    def get_by_slug(self, slug: str) -> Optional[Product]:
        return (
            Product.objects.select_related("category")
            .filter(slug=slug, is_active=True)
            .first()
        )

    def get_by_category(self, category_id: int, active_only: bool = True) -> QuerySet[Product]:
        qs = Product.objects.filter(category_id=category_id).select_related("category")
        if active_only:
            qs = qs.filter(is_active=True)
        return qs.order_by("-created_at")

    def get_active_products(self) -> QuerySet[Product]:
        return Product.objects.filter(is_active=True).select_related("category")

    def search(self, query: str) -> QuerySet[Product]:
        return (
            Product.objects.filter(
                Q(name__icontains=query) | Q(description__icontains=query),
                is_active=True,
            )
            .select_related("category")
            .order_by("-created_at")
        )

    def decrement_stock(self, product_id: int, quantity: int) -> None:
        Product.objects.filter(pk=product_id).update(stock=F("stock") - quantity)
