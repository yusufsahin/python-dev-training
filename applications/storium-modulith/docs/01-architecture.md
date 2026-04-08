# 01 — Mimari Genel Bakış

## N-Katmanlı Mimari Akış Diyagramı

```
HTTP Request
    │
    ▼
┌─────────────────┐
│      View       │  ← Django View / Class-Based View
│   (Controller)  │    Sadece HTTP in/out, iş mantığı YOK
└────────┬────────┘
         │ InputDTO
         ▼
┌─────────────────┐
│    Service      │  ← İş mantığı, validasyon, orkestrasyon
│     Layer       │    Repository'leri çağırır, OutputDTO döner
└────────┬────────┘
         │ Model nesnesi alır/verir
         ▼
┌─────────────────┐
│   Repository    │  ← Veri erişimi (ORM sorguları)
│     Layer       │    Model nesneleri döner, DTO bilmez
└────────┬────────┘
         │ Django ORM
         ▼
┌─────────────────┐
│     Model       │  ← Django ORM Model
│     Layer       │    Alan tanımı + __str__ + Meta + @property
└─────────────────┘
```

---

## Katman Sorumlulukları

### View (Controller) — `apps/<domain>/views.py`
- HTTP request/response yönetimi
- Request verisini Input DTO'ya dönüştürme
- Service çağırma
- Output DTO → template context aktarımı
- Exception → HTTP hata sayfası/redirect (`Http404`, `redirect`)
- **IÇERMEZ**: ORM sorgusu, iş mantığı, e-posta gönderimi

### Service Layer — `core/services/`
- Tek domain'in iş mantığı burada yaşar
- Transaction yönetimi (`@transaction.atomic`)
- Birden fazla Repository orkestre edebilir
- E-posta, bildirim tetiklemesi (NotificationService çağrısı)
- Model nesnelerini Output DTO'ya dönüştürür
- **IÇERMEZ**: Doğrudan ORM import'u (Repository üzerinden gider)

### Repository Layer — `core/repositories/`
- ORM sorgularını kapsüller
- Protocol (interface) + DjangoORM implementasyonu çifti
- Filtreleme, sıralama, sayfalama bu katmanda
- Model nesnesi döner (DTO döndürmez)
- **IÇERMEZ**: İş mantığı, validasyon, e-posta

### DTO Layer — `core/dtos/`
- **Pydantic v2** `BaseModel`; çıktı modelleri `frozen=True` (`ConfigDict`)
- Input DTO: View → Service arası veri taşır (form verisi, query params); doğrulama Pydantic validator’ları ile
- Output DTO: Service → View/Template arası veri taşır
- **IÇERMEZ**: ORM nesnesi, iş mantığı

### Model Layer — `apps/<domain>/models.py`
- Django ORM model tanımları
- Alan (field) tanımları, `__str__`, `Meta`, basit `@property`
- **IÇERMEZ**: Servis çağrısı, e-posta, iş mantığı

---

## Tam Klasör Yapısı

```
storium-modulith/
├── .env.example
├── .gitignore
├── manage.py
├── requirements.txt
│
├── storium/                        ← Django proje paketi
│   ├── __init__.py
│   ├── settings/
│   │   ├── __init__.py             ← DJANGO_ENV okur, ilgili settings'i import eder
│   │   ├── base.py                 ← Ortak ayarlar (INSTALLED_APPS, TEMPLATES, etc.)
│   │   ├── development.py          ← SQLite, DEBUG=True, console e-posta backend
│   │   └── production.py           ← PostgreSQL, DEBUG=False, SMTP e-posta
│   ├── urls.py                     ← Ana URL yönlendirici
│   ├── wsgi.py
│   └── asgi.py
│
├── modules/                        ← Modulith: sınırlandırılmış Django uygulamaları
│   ├── __init__.py
│   ├── catalog/                    ← Kategori + ürün listesi/detay
│   │   ├── __init__.py
│   │   ├── apps.py
│   │   ├── models.py               ← Category, Product
│   │   ├── views.py
│   │   ├── urls.py
│   │   ├── admin.py
│   │   └── migrations/
│   │
│   ├── cart/                       ← Session sepet (model YOK)
│   │   ├── __init__.py
│   │   ├── apps.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   └── context_processors.py  ← Tüm template'lere cart_item_count ekler
│   │
│   ├── orders/                     ← Sipariş
│   │   ├── __init__.py
│   │   ├── apps.py
│   │   ├── models.py               ← Order, OrderItem
│   │   ├── views.py
│   │   ├── urls.py
│   │   ├── admin.py
│   │   └── migrations/
│   │
│   └── notifications/              ← E-posta bildirimleri
│       ├── __init__.py
│       ├── apps.py
│       └── services.py             ← EmailNotificationService
│
├── core/
│   ├── __init__.py
│   ├── repositories/
│   │   ├── __init__.py
│   │   ├── base.py                 ← BaseRepository[T] (Generic)
│   │   ├── protocols.py            ← Protocol (interface) tanımları
│   │   ├── catalog_repository.py   ← DjangoCategoryRepository, DjangoProductRepository
│   │   └── order_repository.py     ← DjangoOrderRepository
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── catalog_service.py      ← CatalogService
│   │   ├── cart_service.py         ← CartService
│   │   └── order_service.py        ← OrderService
│   │
│   ├── dtos/
│   │   ├── __init__.py
│   │   ├── catalog_dtos.py         ← CategoryOutputDTO, ProductOutputDTO, etc.
│   │   ├── cart_dtos.py            ← CartDTO, CartItemDTO
│   │   └── order_dtos.py           ← CheckoutInputDTO, OrderOutputDTO, etc.
│   │
│   └── exceptions/
│       ├── __init__.py
│       └── domain_exceptions.py    ← StoriumBaseException ve alt sınıflar
│
├── templates/
│   ├── base.html                   ← Bootstrap 5 base layout
│   ├── partials/
│   │   ├── _navbar.html
│   │   ├── _footer.html
│   │   ├── _messages.html          ← Django messages framework alert'leri
│   │   ├── _pagination.html
│   │   └── _breadcrumb.html
│   ├── catalog/
│   │   ├── home.html
│   │   ├── product_list.html
│   │   ├── product_detail.html
│   │   └── search_results.html
│   ├── cart/
│   │   └── cart_detail.html
│   ├── orders/
│   │   ├── checkout.html
│   │   ├── order_confirm.html      ← Sipariş tamamlandı sayfası
│   │   ├── order_list.html
│   │   └── order_detail.html
│   └── emails/
│       ├── order_placed_subject.txt
│       ├── order_placed_body.html
│       ├── order_status_subject.txt
│       └── order_status_body.html
│
└── static/
    ├── css/
    │   └── storium.css             ← Özelleştirme CSS (Bootstrap üzerine)
    ├── js/
    │   └── storium.js              ← Minimal JS (cart quantity controls, etc.)
    └── img/
        └── logo.png
```

---

## Dependency Injection Yaklaşımı

Django'da tam DI container kullanmak zorunda değiliz.
Her Service sınıfı, `__init__` metodunda Repository instance'ı alır.
View, Service'i şu şekilde oluşturur:

```python
# apps/catalog/views.py — örnek pattern
from core.repositories.catalog_repository import DjangoCategoryRepository, DjangoProductRepository
from core.services.catalog_service import CatalogService

class ProductListView(View):
    def get(self, request, slug):
        service = CatalogService(
            category_repo=DjangoCategoryRepository(),
            product_repo=DjangoProductRepository(),
        )
        # ...
```

Bu yaklaşım sayesinde:
- Test yazarken Mock repository geçilebilir
- İleride `dependency-injector` kütüphanesi ile değiştirilebilir
- Her view tam kontrole sahip

---

## URL Yapısı (storium/urls.py)

```python
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('modules.catalog.urls')),           # / ve /kategori/ ve /urun/
    path('', include('modules.cart.urls')),              # /sepet/
    path('siparis/', include('modules.orders.urls')),    # /siparis/
]
```

---

## Django App Kayıt Sırası (settings/base.py → INSTALLED_APPS)

```python
INSTALLED_APPS = [
    # Django built-in
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Proje app'leri
    'modules.catalog',
    'modules.cart',
    'modules.orders',
    'modules.notifications',
]
```

---

## Önemli Kurallar (Cursor için)

1. Repository asla DTO import etmez
2. Model asla Service import etmez
3. View asla ORM'e doğrudan erişmez
4. Exception'lar `core/exceptions/domain_exceptions.py`'den gelir
5. Cross-app model erişimi gerekirse Service katmanı orkestre eder
6. Her `POST` view'unda CSRF koruması aktif olmalı (Django default)
7. Order işlemleri `@login_required` dekoratörü gerektirir
