import redis
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.deps import get_redis
from app.exceptions import CategoryNotFoundException, ProductNotFoundException
from app.schemas.catalog import (
    CategoryNavNode,
    CategoryWithProductsDTO,
    ProductDetailDTO,
    ProductListDTO,
    ProductOutputDTO,
)
from app.services import catalog_service

router = APIRouter(prefix="/catalog", tags=["catalog"])


def _redis():
    return get_redis()


@router.get("/featured", response_model=list[ProductOutputDTO])
def featured(
    db: Session = Depends(get_db),
    count: int = Query(default=8, ge=1, le=50),
) -> list[ProductOutputDTO]:
    return catalog_service.get_featured_products(db, count)


@router.get("/nav", response_model=list[CategoryNavNode])
def nav(
    db: Session = Depends(get_db),
    r: redis.Redis = Depends(_redis),
) -> list[CategoryNavNode]:
    return catalog_service.get_category_nav_tree(db, r)


@router.get("/categories/{slug}", response_model=CategoryWithProductsDTO)
def category_detail(
    slug: str,
    db: Session = Depends(get_db),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=12, ge=1, le=48),
) -> CategoryWithProductsDTO:
    try:
        return catalog_service.get_category_with_products(db, slug, page, page_size)
    except CategoryNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e)) from e


@router.get("/products/{slug}", response_model=ProductDetailDTO)
def product_detail(slug: str, db: Session = Depends(get_db)) -> ProductDetailDTO:
    try:
        return catalog_service.get_product_detail(db, slug)
    except ProductNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e)) from e


@router.get("/search", response_model=ProductListDTO)
def search(
    db: Session = Depends(get_db),
    q: str = Query(min_length=1),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=12, ge=1, le=48),
) -> ProductListDTO:
    return catalog_service.search_products(db, q, page, page_size)
