"""Kategoriler API router."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.models.category import Category
from app.schemas.category import CategoryCreate, CategoryResponse

router = APIRouter(prefix="/categories", tags=["categories"])


@router.get("", response_model=list[CategoryResponse])
def list_categories(db: Session = Depends(get_db)):
    """Tüm kategorileri listele."""
    return db.query(Category).order_by(Category.name).all()


@router.post("", response_model=CategoryResponse, status_code=201)
def create_category(body: CategoryCreate, db: Session = Depends(get_db)):
    """Yeni kategori oluştur."""
    cat = Category(name=body.name, color=body.color)
    db.add(cat)
    db.commit()
    db.refresh(cat)
    return cat


@router.delete("/{category_id}", status_code=204)
def delete_category(category_id: int, db: Session = Depends(get_db)):
    """Kategori sil; görevlerdeki category_id null yapılır."""
    cat = db.get(Category, category_id)
    if not cat:
        raise HTTPException(status_code=404, detail="Kategori bulunamadı")
    # Görevlerdeki category_id'yi null yap (SQLAlchemy'de ilişkili task'ları güncelle)
    for task in cat.tasks:
        task.category_id = None
    db.delete(cat)
    db.commit()
    return None
