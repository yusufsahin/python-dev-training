from dataclasses import dataclass, field
from decimal import Decimal
from typing import Optional


@dataclass(frozen=True)
class CategoryOutputDTO:
    id: int
    name: str
    slug: str
    description: str
    is_root: bool
    parent_id: Optional[int] = None
    children_count: int = 0


@dataclass(frozen=True)
class ProductOutputDTO:
    id: int
    name: str
    slug: str
    price: Decimal
    stock: int
    is_in_stock: bool
    category_name: str
    category_slug: str
    description: str = ""
    image_url: Optional[str] = None


@dataclass(frozen=True)
class BreadcrumbItemDTO:
    name: str
    slug: str
    url: str


@dataclass(frozen=True)
class CategoryWithProductsDTO:
    category: CategoryOutputDTO
    products: list[ProductOutputDTO]
    breadcrumb: list[BreadcrumbItemDTO]
    total_count: int
    page: int
    page_size: int
    total_pages: int


@dataclass(frozen=True)
class ProductDetailDTO:
    product: ProductOutputDTO
    breadcrumb: list[BreadcrumbItemDTO]
    related_products: list[ProductOutputDTO] = field(default_factory=list)


@dataclass(frozen=True)
class ProductListDTO:
    products: list[ProductOutputDTO]
    total_count: int
    page: int
    total_pages: int
