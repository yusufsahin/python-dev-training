import redis
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.deps import get_redis, verify_internal_token
from app.exceptions import OutOfStockException, ProductNotFoundException, StoriumBaseException
from app.repositories import catalog_repo
from app.schemas.catalog import InternalProductDTO, StockBatchBody
from app.services import stock_batch

router = APIRouter(tags=["internal"])


@router.get("/internal/products/{product_id}", response_model=InternalProductDTO)
def internal_product(
    product_id: int,
    db: Session = Depends(get_db),
    _: None = Depends(verify_internal_token),
) -> InternalProductDTO:
    p = catalog_repo.product_get_by_id(db, product_id)
    if not p:
        raise HTTPException(status_code=404, detail="Ürün yok")
    return InternalProductDTO(
        id=p.id,
        name=p.name,
        slug=p.slug,
        price=p.price,
        stock=p.stock,
        is_active=p.is_active,
        image_url=p.image_url,
    )


@router.post("/internal/stock/decrement-batch")
def internal_decrement_batch(
    body: StockBatchBody,
    db: Session = Depends(get_db),
    r: redis.Redis = Depends(get_redis),
    _: None = Depends(verify_internal_token),
) -> dict:
    pairs = [(i.product_id, i.quantity) for i in body.items]
    try:
        stock_batch.decrement_batch(db, pairs, r=r)
        db.commit()
    except StoriumBaseException as e:
        db.rollback()
        if isinstance(e, OutOfStockException):
            raise HTTPException(status_code=400, detail=str(e)) from e
        raise HTTPException(status_code=404, detail=str(e)) from e
    return {"ok": True}


@router.post("/internal/stock/increment-batch")
def internal_increment_batch(
    body: StockBatchBody,
    db: Session = Depends(get_db),
    r: redis.Redis = Depends(get_redis),
    _: None = Depends(verify_internal_token),
) -> dict:
    pairs = [(i.product_id, i.quantity) for i in body.items]
    try:
        stock_batch.increment_batch(db, pairs, r=r)
        db.commit()
    except Exception:
        db.rollback()
        raise
    return {"ok": True}
