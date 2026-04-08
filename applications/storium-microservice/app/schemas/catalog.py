from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class CategoryOutputDTO(BaseModel):
    model_config = ConfigDict(frozen=True)

    id: int
    name: str
    slug: str
    description: str
    is_root: bool
    parent_id: Optional[int] = None
    children_count: int = 0


class ProductOutputDTO(BaseModel):
    model_config = ConfigDict(frozen=True)

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


class BreadcrumbItemDTO(BaseModel):
    model_config = ConfigDict(frozen=True)

    name: str
    slug: str
    url: str


class CategoryNavNode(BaseModel):
    model_config = ConfigDict(frozen=True)

    name: str
    slug: str
    children: tuple["CategoryNavNode", ...] = Field(default_factory=tuple)


class CategoryWithProductsDTO(BaseModel):
    model_config = ConfigDict(frozen=True)

    category: CategoryOutputDTO
    products: list[ProductOutputDTO]
    breadcrumb: list[BreadcrumbItemDTO]
    total_count: int
    page: int
    page_size: int
    total_pages: int


class ProductDetailDTO(BaseModel):
    model_config = ConfigDict(frozen=True)

    product: ProductOutputDTO
    breadcrumb: list[BreadcrumbItemDTO]
    related_products: list[ProductOutputDTO] = Field(default_factory=list)


class ProductListDTO(BaseModel):
    model_config = ConfigDict(frozen=True)

    products: list[ProductOutputDTO]
    total_count: int
    page: int
    total_pages: int
