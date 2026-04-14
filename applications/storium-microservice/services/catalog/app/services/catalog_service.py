import json
from typing import Optional

import redis
from sqlalchemy.orm import Session

from app.exceptions import CategoryNotFoundException, ProductNotFoundException
from app.models import Category, Product
from app.repositories import catalog_repo
from app.schemas.catalog import (
    BreadcrumbItemDTO,
    CategoryNavNode,
    CategoryOutputDTO,
    CategoryWithProductsDTO,
    ProductDetailDTO,
    ProductListDTO,
    ProductOutputDTO,
)

_CATEGORY_NAV_CACHE_KEY = "catalog:nav_tree:v1"
_CATEGORY_NAV_CACHE_TTL = 300


def invalidate_category_nav_cache(r: Optional[redis.Redis]) -> None:
    if r is not None:
        r.delete(_CATEGORY_NAV_CACHE_KEY)


def _breadcrumb_for_category(category: Category) -> list[BreadcrumbItemDTO]:
    items: list[BreadcrumbItemDTO] = []
    for anc in category.ancestors():
        items.append(
            BreadcrumbItemDTO(
                name=anc.name,
                slug=anc.slug,
                url=f"/category/{anc.slug}",
            ),
        )
    items.append(
        BreadcrumbItemDTO(
            name=category.name,
            slug=category.slug,
            url=f"/category/{category.slug}",
        ),
    )
    return items


def _category_to_dto(db: Session, category: Category) -> CategoryOutputDTO:
    cc = catalog_repo.category_children_count(db, category.id)
    return CategoryOutputDTO(
        id=category.id,
        name=category.name,
        slug=category.slug,
        description=category.description or "",
        is_root=category.is_root,
        parent_id=category.parent_id,
        children_count=cc,
    )


def _product_to_dto(product: Product) -> ProductOutputDTO:
    return ProductOutputDTO(
        id=product.id,
        name=product.name,
        slug=product.slug,
        price=product.price,
        stock=product.stock,
        is_in_stock=product.is_in_stock,
        description=product.description or "",
        image_url=product.image_url,
        category_name=product.category.name,
        category_slug=product.category.slug,
    )


def get_root_categories(db: Session) -> list[CategoryOutputDTO]:
    cats = catalog_repo.category_get_roots(db)
    return [_category_to_dto(db, c) for c in cats]


def get_category_with_products(
    db: Session,
    category_slug: str,
    page: int = 1,
    page_size: int = 12,
) -> CategoryWithProductsDTO:
    category = catalog_repo.category_get_by_slug(db, category_slug)
    if not category:
        raise CategoryNotFoundException(f"Kategori bulunamadı: {category_slug}")

    total = catalog_repo.product_count_by_category(db, category.id)
    products = catalog_repo.product_page_by_category(
        db,
        category.id,
        page=page,
        page_size=page_size,
    )
    total_pages = max(1, (total + page_size - 1) // page_size) if total else 1
    if page > total_pages and total > 0:
        page = total_pages

    return CategoryWithProductsDTO(
        category=_category_to_dto(db, category),
        products=[_product_to_dto(p) for p in products],
        breadcrumb=_breadcrumb_for_category(category),
        total_count=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages,
    )


def get_product_detail(db: Session, product_slug: str) -> ProductDetailDTO:
    product = catalog_repo.product_get_by_slug(db, product_slug)
    if not product:
        raise ProductNotFoundException(f"Ürün bulunamadı: {product_slug}")

    related = catalog_repo.product_get_by_category(db, product.category_id)
    related_four = [_product_to_dto(p) for p in related if p.id != product.id][:4]

    return ProductDetailDTO(
        product=_product_to_dto(product),
        breadcrumb=_breadcrumb_for_category(product.category),
        related_products=related_four,
    )


def search_products(
    db: Session,
    query: str,
    page: int = 1,
    page_size: int = 12,
) -> ProductListDTO:
    rows, total = catalog_repo.product_search(db, query, page=page, page_size=page_size)
    total_pages = max(1, (total + page_size - 1) // page_size) if total else 1
    return ProductListDTO(
        products=[_product_to_dto(p) for p in rows],
        total_count=total,
        page=page,
        total_pages=total_pages,
    )


def get_featured_products(db: Session, count: int = 8) -> list[ProductOutputDTO]:
    rows = catalog_repo.product_active_in_stock_slice(db, count)
    return [_product_to_dto(p) for p in rows]


def get_category_nav_tree(db: Session, r: Optional[redis.Redis]) -> list[CategoryNavNode]:
    if r is not None:
        raw = r.get(_CATEGORY_NAV_CACHE_KEY)
        if raw:
            data = json.loads(raw)
            return [CategoryNavNode.model_validate(x) for x in data]

    roots = catalog_repo.category_get_roots(db)
    result: list[CategoryNavNode] = []
    for root in roots:
        children = catalog_repo.category_active_children(db, root.id)
        node = CategoryNavNode(
            name=root.name,
            slug=root.slug,
            children=tuple(
                CategoryNavNode(name=c.name, slug=c.slug, children=())
                for c in children
            ),
        )
        result.append(node)

    if r is not None:
        r.setex(
            _CATEGORY_NAV_CACHE_KEY,
            _CATEGORY_NAV_CACHE_TTL,
            json.dumps([n.model_dump(mode="json") for n in result]),
        )
    return result
