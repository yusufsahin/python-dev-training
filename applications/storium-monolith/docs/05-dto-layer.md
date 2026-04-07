# 05 — DTO Katmanı

## Genel Kurallar
- Tüm DTO'lar `@dataclass` ile tanımlanır
- Output DTO'lar `frozen=True` — immutable, template render'ı güvenli
- Input DTO'lar mutable (`frozen=False`) — validasyon metodu içerebilir
- ORM nesnesi içermez, servis sınıfı içermez
- `Optional` alanlar için `field(default=None)` kullanılır
- Dosya konumları: `core/dtos/`

---

## Catalog DTO'ları (core/dtos/catalog_dtos.py)

```python
from dataclasses import dataclass, field
from decimal import Decimal
from typing import Optional


# ── Output DTOs ──────────────────────────────────────────────────────────────

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
    description: str = ''
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
```

---

## Cart DTO'ları (core/dtos/cart_dtos.py)

```python
from dataclasses import dataclass
from decimal import Decimal
from typing import Optional


@dataclass(frozen=True)
class CartItemDTO:
    product_id: int
    name: str
    price: Decimal
    quantity: int
    image_url: Optional[str]

    @property
    def line_total(self) -> Decimal:
        return self.price * self.quantity


@dataclass(frozen=True)
class CartDTO:
    items: list[CartItemDTO]
    total_price: Decimal
    item_count: int         # Toplam adet (tüm quantity toplamı)
    unique_item_count: int  # Farklı ürün sayısı (len(items))
```

**Kullanım notu**: `frozen=True` dataclass'ta `@property` kullanmak için Python 3.10+ gerekir.
Python 3.9 kullanılıyorsa `@property` yerine method olarak tanımlanabilir veya `frozen=False` yapılabilir.

---

## Order DTO'ları (core/dtos/order_dtos.py)

```python
from dataclasses import dataclass, field
from decimal import Decimal
from typing import Optional


# ── Input DTOs ────────────────────────────────────────────────────────────────

@dataclass
class CheckoutInputDTO:
    """Checkout formundan gelen veri."""
    shipping_name: str
    shipping_address: str
    shipping_city: str
    shipping_phone: str = ''
    notes: str = ''

    def validate(self) -> list[str]:
        """
        Saf Python validasyonu.
        Hata mesajları listesi döner. Boşsa validasyon geçti.
        Django Form validasyonuna ek güvence katmanı.
        """
        errors = []
        if not self.shipping_name.strip():
            errors.append("Ad Soyad zorunludur.")
        if not self.shipping_address.strip():
            errors.append("Adres zorunludur.")
        if not self.shipping_city.strip():
            errors.append("Şehir zorunludur.")
        return errors

    @classmethod
    def from_post(cls, post_data: dict) -> 'CheckoutInputDTO':
        """Django request.POST dict'inden oluşturur."""
        return cls(
            shipping_name=post_data.get('shipping_name', '').strip(),
            shipping_address=post_data.get('shipping_address', '').strip(),
            shipping_city=post_data.get('shipping_city', '').strip(),
            shipping_phone=post_data.get('shipping_phone', '').strip(),
            notes=post_data.get('notes', '').strip(),
        )


# ── Output DTOs ───────────────────────────────────────────────────────────────

@dataclass(frozen=True)
class OrderItemOutputDTO:
    product_id: int
    product_name: str
    unit_price: Decimal
    quantity: int
    line_total: Decimal


@dataclass(frozen=True)
class OrderOutputDTO:
    id: int
    status: str                     # 'pending', 'confirmed', etc.
    status_display: str             # 'Beklemede', 'Onaylandı', etc.
    total_price: Decimal
    shipping_name: str
    shipping_address: str
    shipping_city: str
    shipping_phone: str
    notes: str
    items: list[OrderItemOutputDTO]
    created_at: str                 # ISO format string
    updated_at: str                 # ISO format string
```

---

## DTO Dönüşüm Akışı

```
View (request.POST)
    │
    ├── CheckoutInputDTO.from_post(request.POST)
    │         → CheckoutInputDTO
    │
    ▼
Service (iş mantığı)
    │
    ├── _order_to_dto(order_model_instance)
    │         → OrderOutputDTO
    │
    ▼
View / Template
    │
    └── {{ order.status_display }}  ← immutable, güvenli
```

---

## Template'de DTO Kullanımı

DTO alanlarına template'de doğrudan erişilir:

```html
<!-- catalog/product_detail.html -->
<h1>{{ data.product.name }}</h1>
<p>{{ data.product.display_price }}</p>  <!-- NOT: display_price Model'de @property -->

{% if data.product.is_in_stock %}
  <button>Sepete Ekle</button>
{% else %}
  <span class="badge bg-danger">Stokta Yok</span>
{% endif %}

<!-- Breadcrumb -->
{% for crumb in data.breadcrumb %}
  <a href="{{ crumb.url }}">{{ crumb.name }}</a>
{% endfor %}

<!-- Cart -->
{{ cart.item_count }}   ← context_processor'dan gelir
{{ cart.total_price }}
```

---

## Önemli Notlar

1. `frozen=True` DTO'lar değiştirilemez — template'e geçildikten sonra güvenlidir
2. `CheckoutInputDTO.validate()` Service çağrılmadan önce View'da kontrol edilir
3. `CartItemDTO.line_total` hesaplanmış alan; veritabanına yazılmaz
4. `OrderOutputDTO.status_display` insan okunabilir durum; template'de doğrudan kullanılır
5. Tüm para alanları `Decimal` tipinde — float kullanılmaz (kayan nokta hataları)
