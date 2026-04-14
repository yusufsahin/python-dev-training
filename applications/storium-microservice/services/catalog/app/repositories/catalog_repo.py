from typing import Optional

from sqlalchemy import Select, func, or_, select
from sqlalchemy.orm import Session, selectinload

from app.models import Category, Product


def category_get_by_slug(db: Session, slug: str) -> Optional[Category]:
    return db.scalar(
        select(Category).where(Category.slug == slug, Category.is_active.is_(True)),
    )


def category_get_roots(db: Session) -> list[Category]:
    return list(
        db.scalars(
            select(Category)
            .where(Category.parent_id.is_(None), Category.is_active.is_(True))
            .order_by(Category.name),
        ).all(),
    )


def category_active_children(db: Session, parent_id: int) -> list[Category]:
    return list(
        db.scalars(
            select(Category)
            .where(Category.parent_id == parent_id, Category.is_active.is_(True))
            .order_by(Category.name),
        ).all(),
    )


def category_children_count(db: Session, parent_id: int) -> int:
    return (
        db.scalar(
            select(func.count())
            .select_from(Category)
            .where(Category.parent_id == parent_id, Category.is_active.is_(True)),
        )
        or 0
    )


def product_get_by_id(db: Session, pk: int) -> Optional[Product]:
    return db.scalar(
        select(Product)
        .options(selectinload(Product.category))
        .where(Product.id == pk),
    )


def product_get_by_slug(db: Session, slug: str) -> Optional[Product]:
    return db.scalar(
        select(Product)
        .options(selectinload(Product.category))
        .where(Product.slug == slug, Product.is_active.is_(True)),
    )


def _product_category_base() -> Select[tuple[Product]]:
    return select(Product).options(selectinload(Product.category))


def product_get_by_category(
    db: Session,
    category_id: int,
    *,
    active_only: bool = True,
) -> list[Product]:
    q = _product_category_base().where(Product.category_id == category_id)
    if active_only:
        q = q.where(Product.is_active.is_(True))
    q = q.order_by(Product.created_at.desc())
    return list(db.scalars(q).all())


def product_count_by_category(db: Session, category_id: int, *, active_only: bool = True) -> int:
    stmt = select(func.count()).select_from(Product).where(Product.category_id == category_id)
    if active_only:
        stmt = stmt.where(Product.is_active.is_(True))
    return db.scalar(stmt) or 0


def product_page_by_category(
    db: Session,
    category_id: int,
    *,
    page: int,
    page_size: int,
    active_only: bool = True,
) -> list[Product]:
    offset = (page - 1) * page_size
    q = _product_category_base().where(Product.category_id == category_id)
    if active_only:
        q = q.where(Product.is_active.is_(True))
    q = q.order_by(Product.created_at.desc()).offset(offset).limit(page_size)
    return list(db.scalars(q).all())


def product_search(
    db: Session,
    query: str,
    *,
    page: int,
    page_size: int,
) -> tuple[list[Product], int]:
    term = f"%{query.strip()}%"
    base = (
        select(Product)
        .options(selectinload(Product.category))
        .where(
            Product.is_active.is_(True),
            or_(Product.name.ilike(term), Product.description.ilike(term)),
        )
    )
    count_stmt = (
        select(func.count()).select_from(Product).where(
            Product.is_active.is_(True),
            or_(Product.name.ilike(term), Product.description.ilike(term)),
        )
    )
    total = db.scalar(count_stmt) or 0
    offset = (page - 1) * page_size
    rows = list(
        db.scalars(
            base.order_by(Product.created_at.desc()).offset(offset).limit(page_size),
        ).all(),
    )
    return rows, total


def product_active_in_stock_slice(db: Session, limit: int) -> list[Product]:
    return list(
        db.scalars(
            select(Product)
            .options(selectinload(Product.category))
            .where(Product.is_active.is_(True), Product.stock > 0)
            .order_by(Product.created_at.desc())
            .limit(limit),
        ).all(),
    )


def product_decrement_stock(db: Session, product_id: int, quantity: int) -> None:
    p = db.get(Product, product_id)
    if p is not None:
        p.stock = max(0, int(p.stock) - quantity)
        db.add(p)


def product_increment_stock(db: Session, product_id: int, quantity: int) -> None:
    p = db.get(Product, product_id)
    if p is not None:
        p.stock = int(p.stock) + quantity
        db.add(p)
