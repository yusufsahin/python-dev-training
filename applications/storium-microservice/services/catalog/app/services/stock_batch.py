"""Servisler arası stok toplu güncelleme (tek transaction)."""

from sqlalchemy.orm import Session

from app.exceptions import OutOfStockException, ProductNotFoundException
from app.repositories import catalog_repo


def decrement_batch(db: Session, items: list[tuple[int, int]], *, r=None) -> None:
    from app.services import catalog_service

    for product_id, quantity in items:
        p = catalog_repo.product_get_by_id(db, product_id)
        if not p or not p.is_active:
            raise ProductNotFoundException(f"Ürün bulunamadı: id={product_id}")
        if p.stock < quantity:
            raise OutOfStockException(p.name, p.stock)
    for product_id, quantity in items:
        catalog_repo.product_decrement_stock(db, product_id, quantity)
    db.flush()
    catalog_service.invalidate_category_nav_cache(r)


def increment_batch(db: Session, items: list[tuple[int, int]], *, r=None) -> None:
    from app.services import catalog_service

    for product_id, quantity in items:
        catalog_repo.product_increment_stock(db, product_id, quantity)
    db.flush()
    catalog_service.invalidate_category_nav_cache(r)
