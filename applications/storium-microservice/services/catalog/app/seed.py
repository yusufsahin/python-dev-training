"""Katalog seed (kategori + ürün)."""
from __future__ import annotations

from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Category, Product


SEED_CATEGORIES = [
    {
        "name": "Elektronik",
        "slug": "elektronik",
        "description": "Bilgisayar, ses ve mobil aksesuarlar.",
        "parent_slug": None,
    },
    {
        "name": "Bilgisayar Aksesuarları",
        "slug": "bilgisayar-aksesuarlari",
        "description": "Klavye, mouse, kablolar.",
        "parent_slug": "elektronik",
    },
    {
        "name": "Ev ve Yaşam",
        "slug": "ev-yasam",
        "description": "Mutfak, dekorasyon ve günlük kullanım.",
        "parent_slug": None,
    },
    {
        "name": "Kitap",
        "slug": "kitap",
        "description": "Roman, teknik ve çocuk kitapları.",
        "parent_slug": None,
    },
]

def _picsum(slug: str) -> str:
    """Slug ile deterministik demo görsel (picsum.photos)."""
    return f"https://picsum.photos/seed/{slug}/640/480"


SEED_PRODUCTS = [
    {
        "category_slug": "elektronik",
        "name": "Kablosuz Kulaklık Pro",
        "slug": "kablosuz-kulaklik-pro",
        "description": "Gürültü önleyici, 30 saat pil ömrü.",
        "price": Decimal("1299.90"),
        "stock": 25,
        "image_url": _picsum("kablosuz-kulaklik-pro"),
    },
    {
        "category_slug": "elektronik",
        "name": "Taşınabilir Bluetooth Hoparlör",
        "slug": "tasinabilir-bluetooth-hoparlor",
        "description": "IPX7 su geçirmez, kompakt tasarım.",
        "price": Decimal("549.00"),
        "stock": 40,
        "image_url": _picsum("tasinabilir-bluetooth-hoparlor"),
    },
    {
        "category_slug": "bilgisayar-aksesuarlari",
        "name": "Mekanik Klavye RGB",
        "slug": "mekanik-klavye-rgb",
        "description": "Hot-swap anahtarlar, Türkçe Q düzeni.",
        "price": Decimal("1899.00"),
        "stock": 15,
        "image_url": _picsum("mekanik-klavye-rgb"),
    },
    {
        "category_slug": "bilgisayar-aksesuarlari",
        "name": "USB-C Hub 7 in 1",
        "slug": "usb-c-hub-7-in-1",
        "description": "HDMI, USB-A, SD ve güç dağıtımı.",
        "price": Decimal("449.50"),
        "stock": 60,
        "image_url": _picsum("usb-c-hub-7-in-1"),
    },
    {
        "category_slug": "ev-yasam",
        "name": "Kahve Fincanı Seti",
        "slug": "kahve-fincani-seti",
        "description": "Porselen 2 kişilik set.",
        "price": Decimal("149.90"),
        "stock": 100,
        "image_url": _picsum("kahve-fincani-seti"),
    },
    {
        "category_slug": "ev-yasam",
        "name": "Bambu Kesme Tahtası",
        "slug": "bambu-kesme-tahtasi",
        "description": "Doğal bambu, 35x25 cm.",
        "price": Decimal("89.00"),
        "stock": 0,
        "image_url": _picsum("bambu-kesme-tahtasi"),
    },
    {
        "category_slug": "kitap",
        "name": "Python ile Veri Analizi",
        "slug": "python-ile-veri-analizi",
        "description": "Pandas ve NumPy ile pratik örnekler.",
        "price": Decimal("312.00"),
        "stock": 20,
        "image_url": _picsum("python-ile-veri-analizi"),
    },
    {
        "category_slug": "kitap",
        "name": "FastAPI ile Web API",
        "slug": "fastapi-ile-web-api",
        "description": "Modern Python API geliştirme.",
        "price": Decimal("275.00"),
        "stock": 12,
        "image_url": _picsum("fastapi-ile-web-api"),
    },
]


def run_seed(db: Session) -> None:
    slug_to_category: dict[str, Category] = {}

    for row in SEED_CATEGORIES:
        parent = None
        if row["parent_slug"]:
            parent = slug_to_category.get(row["parent_slug"])
            if parent is None:
                parent = db.scalar(select(Category).where(Category.slug == row["parent_slug"]))
        existing = db.scalar(select(Category).where(Category.slug == row["slug"]))
        if existing:
            existing.name = row["name"]
            existing.description = row["description"]
            existing.parent = parent
            existing.is_active = True
            cat = existing
        else:
            cat = Category(
                name=row["name"],
                slug=row["slug"],
                description=row["description"],
                parent=parent,
                is_active=True,
            )
            db.add(cat)
            db.flush()
        slug_to_category[row["slug"]] = cat

    for row in SEED_PRODUCTS:
        cat = slug_to_category.get(row["category_slug"])
        if cat is None:
            cat = db.scalar(select(Category).where(Category.slug == row["category_slug"]))
        if cat is None:
            continue
        existing_p = db.scalar(select(Product).where(Product.slug == row["slug"]))
        if existing_p:
            existing_p.category = cat
            existing_p.name = row["name"]
            existing_p.description = row["description"]
            existing_p.price = row["price"]
            existing_p.stock = row["stock"]
            existing_p.image_url = row.get("image_url")
            existing_p.is_active = True
        else:
            db.add(
                Product(
                    category=cat,
                    name=row["name"],
                    slug=row["slug"],
                    description=row["description"],
                    price=row["price"],
                    stock=row["stock"],
                    image_url=row.get("image_url"),
                    is_active=True,
                ),
            )

    db.flush()


def main() -> None:
    from app.database import SessionLocal

    db = SessionLocal()
    try:
        run_seed(db)
        db.commit()
        print("Catalog seed OK.")
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()
