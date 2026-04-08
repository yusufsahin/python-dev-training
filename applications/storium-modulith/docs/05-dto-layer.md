# 05 — DTO Katmanı

## Genel Kurallar

- Tüm DTO’lar **Pydantic v2** `BaseModel` ile tanımlanır (`pydantic>=2,<3`, `requirements.txt`).
- Çıktı (output) DTO’lar `model_config = ConfigDict(frozen=True)` — değişmez, şablon bağlamı için güvenli.
- Girdi (input) DTO’lar (`CheckoutInputDTO`) doğrulamayı `field_validator` ve `model_validate` ile yapar; `ConfigDict(str_strip_whitespace=True)` ile form alanları kırpılır.
- ORM nesnesi içermez, servis sınıfı içermez.
- İsteğe bağlı alanlar: `Optional[...] = None` veya `Field(default_factory=...)`.
- Dosya konumları: `core/dtos/`; paket dışa aktarım: `core/dtos/__init__.py`.

---

## Catalog DTO’ları (`core/dtos/catalog_dtos.py`)

Özet: `CategoryOutputDTO`, `ProductOutputDTO`, `BreadcrumbItemDTO`, `CategoryWithProductsDTO`, `ProductDetailDTO`, `ProductListDTO` — hepsi `BaseModel` + `frozen=True`. Navigasyon ağacı:

```python
class CategoryNavNode(BaseModel):
    model_config = ConfigDict(frozen=True)

    name: str
    slug: str
    children: tuple["CategoryNavNode", ...] = Field(default_factory=tuple)
```

`CatalogService.get_category_nav_tree()` çocuk düğümleri `tuple(...)` ile üretir; şablonlar yalnızca iterable gerektirir.

---

## Cart DTO’ları (`core/dtos/cart_dtos.py`)

```python
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, ConfigDict, computed_field


class CartItemDTO(BaseModel):
    model_config = ConfigDict(frozen=True)

    product_id: int
    name: str
    price: Decimal
    quantity: int
    image_url: Optional[str] = None

    @computed_field
    def line_total(self) -> Decimal:
        return self.price * self.quantity


class CartDTO(BaseModel):
    model_config = ConfigDict(frozen=True)

    items: list[CartItemDTO]
    total_price: Decimal
    item_count: int         # Toplam adet (tüm quantity toplamı)
    unique_item_count: int  # Farklı ürün sayısı (len(items))
```

`line_total` veritabanına yazılmaz; şablonda `{{ item.line_total }}` ile kullanılır.

---

## Order DTO’ları (`core/dtos/order_dtos.py`)

Girdi: `CheckoutInputDTO` — `from_post(request.POST)` içinde `model_validate` kullanır; boş zorunlu alanlarda `ValidationError` fırlatır. Türkçe mesajlar `field_validator` içinde `ValueError("...")` ile verilir.

View tarafında hata metinleri `checkout_validation_messages(exc)` ile üretilir (Pydantic’in `Value error, ` öneki temizlenir).

Çıktı: `OrderItemOutputDTO`, `OrderOutputDTO` — `frozen=True`, alanlar önceki sözleşmeyle aynı (`status_display`, `items`, ISO tarih string’leri, vb.).

---

## DTO Dönüşüm Akışı (Checkout)

```
View (request.POST)
    │
    ├── try: CheckoutInputDTO.from_post(request.POST)
    │         except ValidationError → checkout_validation_messages → messages.error
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
    └── {{ order.status_display }}  ← frozen model, alan erişimi aynı
```

---

## Template'de DTO Kullanımı

DTO alanlarına template'de doğrudan erişilir (Pydantic model örnekleri alanlara attribute ile erişilir; şablon motoru bunları okur):

```html
<!-- catalog/product_detail.html -->
<h1>{{ data.product.name }}</h1>

{% if data.product.is_in_stock %}
  <button>Sepete Ekle</button>
{% else %}
  <span class="badge bg-danger">Stokta Yok</span>
{% endif %}

{% for crumb in data.breadcrumb %}
  <a href="{{ crumb.url }}">{{ crumb.name }}</a>
{% endfor %}

<!-- Cart -->
{{ cart.item_count }}
{{ cart.total_price }}
```

---

## Önemli Notlar

1. `frozen=True` çıktı DTO’ları değiştirilemez — şablona geçirildikten sonra güvenli kabul edilir.
2. Checkout doğrulaması View’da `ValidationError` yakalanarak yapılır; `validate()` adlı ayrı bir liste metodu yoktur.
3. `CartItemDTO.line_total` Pydantic `@computed_field` ile hesaplanır; veritabanına yazılmaz.
4. `OrderOutputDTO.status_display` insan okunabilir durum; template'de doğrudan kullanılır.
5. Para alanları `Decimal` — float kullanılmaz.
6. İleride REST API eklenirse aynı modeller `model_dump()` / `model_dump_json()` ile serileştirilebilir.
