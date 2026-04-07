from django.core.paginator import Paginator
from django.urls import reverse

from core.dtos.catalog_dtos import (
    BreadcrumbItemDTO,
    CategoryOutputDTO,
    CategoryWithProductsDTO,
    ProductDetailDTO,
    ProductListDTO,
    ProductOutputDTO,
)
from core.exceptions.domain_exceptions import CategoryNotFoundException, ProductNotFoundException
from core.repositories.protocols import CategoryRepositoryProtocol, ProductRepositoryProtocol


class CatalogService:
    def __init__(
        self,
        category_repo: CategoryRepositoryProtocol,
        product_repo: ProductRepositoryProtocol,
    ):
        self.category_repo = category_repo
        self.product_repo = product_repo

    def get_root_categories(self) -> list[CategoryOutputDTO]:
        categories = self.category_repo.get_root_categories()
        return [self._category_to_dto(c) for c in categories]

    def get_category_with_products(
        self,
        category_slug: str,
        page: int = 1,
        page_size: int = 12,
    ) -> CategoryWithProductsDTO:
        category = self.category_repo.get_by_slug(category_slug)
        if not category:
            raise CategoryNotFoundException(f"Kategori bulunamadı: {category_slug}")

        product_qs = self.product_repo.get_by_category(category.id)
        paginator = Paginator(product_qs, page_size)
        page_obj = paginator.get_page(page)

        return CategoryWithProductsDTO(
            category=self._category_to_dto(category),
            products=[self._product_to_dto(p) for p in page_obj.object_list],
            breadcrumb=self._build_breadcrumb(category),
            total_count=paginator.count,
            page=page_obj.number,
            page_size=page_size,
            total_pages=paginator.num_pages,
        )

    def get_product_detail(self, product_slug: str) -> ProductDetailDTO:
        product = self.product_repo.get_by_slug(product_slug)
        if not product:
            raise ProductNotFoundException(f"Ürün bulunamadı: {product_slug}")

        related_qs = self.product_repo.get_by_category(product.category_id).exclude(pk=product.pk)[:4]

        return ProductDetailDTO(
            product=self._product_to_dto(product),
            breadcrumb=self._build_breadcrumb(product.category),
            related_products=[self._product_to_dto(p) for p in related_qs],
        )

    def search_products(self, query: str, page: int = 1, page_size: int = 12) -> ProductListDTO:
        product_qs = self.product_repo.search(query)
        paginator = Paginator(product_qs, page_size)
        page_obj = paginator.get_page(page)

        return ProductListDTO(
            products=[self._product_to_dto(p) for p in page_obj.object_list],
            total_count=paginator.count,
            page=page_obj.number,
            total_pages=paginator.num_pages,
        )

    def get_featured_products(self, count: int = 8) -> list[ProductOutputDTO]:
        qs = self.product_repo.get_active_products().filter(stock__gt=0)[:count]
        return [self._product_to_dto(p) for p in qs]

    def _category_to_dto(self, category) -> CategoryOutputDTO:
        return CategoryOutputDTO(
            id=category.id,
            name=category.name,
            slug=category.slug,
            description=category.description or "",
            is_root=category.is_root,
            parent_id=category.parent_id,
            children_count=category.children.filter(is_active=True).count(),
        )

    def _product_to_dto(self, product) -> ProductOutputDTO:
        return ProductOutputDTO(
            id=product.id,
            name=product.name,
            slug=product.slug,
            price=product.price,
            stock=product.stock,
            is_in_stock=product.is_in_stock,
            description=product.description or "",
            image_url=product.image.url if product.image else None,
            category_name=product.category.name,
            category_slug=product.category.slug,
        )

    def _build_breadcrumb(self, category) -> list[BreadcrumbItemDTO]:
        ancestors = category.get_ancestors()
        breadcrumb: list[BreadcrumbItemDTO] = []
        for anc in ancestors:
            breadcrumb.append(
                BreadcrumbItemDTO(
                    name=anc.name,
                    slug=anc.slug,
                    url=reverse("catalog:category_detail", kwargs={"slug": anc.slug}),
                ),
            )
        breadcrumb.append(
            BreadcrumbItemDTO(
                name=category.name,
                slug=category.slug,
                url=reverse("catalog:category_detail", kwargs={"slug": category.slug}),
            ),
        )
        return breadcrumb
