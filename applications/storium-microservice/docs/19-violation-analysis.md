# 19 — Mevcut Microservice İhlalleri Analizi

Bu belge, `storium-microservice` projesindeki mikroservis mimarisi ihlallerini, **tam dosya yolları ve kod satırlarıyla** belgeler. Geçiş planı için kaynak belge olarak kullanılır; uygulama adımları [20-phase0-1-infra-gateway.md](20-phase0-1-infra-gateway.md) – [24-phase5-observability.md](24-phase5-observability.md) dosyalarındadır.

---

## Proje Mevcut Durumu

| Özellik | Durum |
|---------|-------|
| Mimari | Modüler Monolit (tek FastAPI uygulaması) |
| Deploy birimi | Tek Docker image (`Dockerfile`) |
| Veritabanı | Tek PostgreSQL (`storium_db`) |
| Cache | Tek Redis (sepet + nav cache) |
| Mesaj kuyruğu | **Yok** |
| API Gateway | **Yok** |
| Servis keşfi | **Yok** |

---

## İhlal #1 — Paylaşılan Tek Veritabanı (KRİTİK)

Tüm servisler (Auth, Catalog, Cart, Orders) aynı PostgreSQL veritabanına bağlanıyor.

**Etkilenen dosyalar:**

```
app/database.py          → tek engine, tek SessionLocal
app/models.py            → User + Category + Product + Order + OrderItem hepsi burada
app/config.py:13         → database_url tek ayar
docker-compose.yml:17-31 → tek `db` servisi, tek POSTGRES_DB
```

**`app/database.py` (sorunlu bölüm):**
```python
engine = create_engine(
    _settings.database_url,   # tek bağlantı dizisi
    pool_pre_ping=True,
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
```

**Neden ihlal:** Servisler birbirinin tablolarına doğrudan erişebilir; şema değişikliği tüm servisleri etkiler; bağımsız ölçekleme imkânsız.

---

## İhlal #2 — Servisler Arası Direkt Python Import (KRİTİK)

Farklı domain'lere ait modüller birbirini doğrudan import ediyor.

### 2a. Orders → Catalog DB erişimi

**`app/services/order_service.py:11`**
```python
from app.repositories import catalog_repo, order_repo
```

**Kullanım yerleri:**
```python
# satır 40: Catalog domain'inin DB'sine doğrudan yazma
product = catalog_repo.product_get_by_id(self._db, item.product_id)

# satır 70: Catalog tablolarını Orders context'inden değiştirme
catalog_repo.product_decrement_stock(self._db, item.product_id, item.quantity)
```

### 2b. Orders Router → Cart Service import

**`app/routers/orders.py:18`**
```python
from app.services import cart_service
```

**Kullanım yerleri:**
```python
# satır 48
cart = cart_service.get_cart(r, cart_id)
# satır 54
cart_service.clear_cart(r, cart_id)
```

### 2c. Cart → Catalog DB erişimi

**`app/services/cart_service.py:9`**
```python
from app.repositories import catalog_repo
```

**Kullanım yerleri:**
```python
# satır 75: sepete ürün eklerken Catalog DB'yi sorgulama
product = catalog_repo.product_get_by_id(db, product_id)

# satır 108: ürün güncelleme sırasında stok kontrolü
product = catalog_repo.product_get_by_id(db, product_id)
```

### 2d. Notifications → User DB erişimi

**`app/services/notifications.py:7`**
```python
from app.repositories import user_repo
```

**Kullanım yerleri:**
```python
# satır 17: sipariş e-postası için Identity domain'inin DB'sini sorgulama
user = user_repo.user_get_by_id(self._db, self._user_id_for_order(order.id))
```

---

## İhlal #3 — Paylaşılan Model Dosyası (YÜKSEK)

**`app/models.py`** tek dosyada beş farklı domain'in ORM modelini barındırıyor:

| Satır | Model | Sahip Domain |
|-------|-------|--------------|
| 15-24 | `User` | Identity |
| 27-56 | `Category` | Catalog |
| 59-83 | `Product` | Catalog |
| 85-109 | `Order` | Orders |
| 112-127 | `OrderItem` | Orders |

`OrderItem.product_id` → `products.id` FK ilişkisi, Orders domain'ini Catalog domain'ine yapısal olarak bağlıyor (V1 ile örtüşür).

---

## İhlal #4 — API Gateway Yok (YÜKSEK)

**`app/main.py:19-22`** — Tek FastAPI uygulaması, tüm router'ları doğrudan mount ediyor:
```python
app.include_router(auth.router, prefix="/api")
app.include_router(catalog.router, prefix="/api")
app.include_router(cart.router, prefix="/api")
app.include_router(orders.router, prefix="/api")
```

**`frontend/src/lib/api.js:2`** — Frontend doğrudan API sunucusuna bağlanıyor:
```javascript
function getPrefix() {
  return process.env.NEXT_PUBLIC_API_BASE ?? "";
}
```

**`docker-compose.yml:77`** — UI build sırasında API adresi hard-code ediliyor:
```yaml
args:
  NEXT_PUBLIC_API_BASE: http://localhost:${DOCKER_API_PORT:-8001}
```

---

## İhlal #5 — Senkron Servis Zinciri (YÜKSEK)

Checkout akışı tek request içinde dört farklı domain'i bloklayarak çağırıyor:

```
POST /api/orders/checkout
 │
 ├─ cart_service.get_cart()         [Redis okuma — senkron]
 │
 ├─ for item in cart.items:
 │    catalog_repo.product_get_by_id()    [Catalog DB — senkron, V2a]
 │
 ├─ order_repo.order_create()            [Orders DB — senkron]
 │
 ├─ for item in cart.items:
 │    catalog_repo.product_decrement_stock() [Catalog DB yazma — senkron, V2a]
 │
 ├─ EmailNotificationService.send_order_placed()
 │    ├─ user_repo.user_get_by_id()     [Identity DB — senkron, V2d]
 │    └─ smtplib.SMTP(...).sendmail()   [Blocking SMTP — senkron, V10]
 │
 └─ cart_service.clear_cart()           [Redis silme — senkron]
```

**Sorun:** SMTP sunucu yavaşsa veya Catalog DB kilitlenirse tüm checkout isteği engellenir. Bir servisin arızası diğerlerine yayılır (cascade failure).

---

## İhlal #6 — Tek Deploy Birimi (YÜKSEK)

**`Dockerfile`** — Tüm servisler tek image olarak paketleniyor.
**`docker-compose.yml:33-70`** — Tek `api` container, tüm router'ları çalıştırıyor.

Sonuç: Catalog servisini ölçeklendirmek için tüm uygulamayı kopyalamak gerekiyor.

---

## İhlal #7 — Monolitik Konfigürasyon (ORTA)

**`app/config.py`** — Tüm servisler için tek `Settings` sınıfı:
```python
class Settings(BaseSettings):
    secret_key: str = ...        # Identity servisi
    database_url: str = ...      # Tüm servisler
    redis_url: str = ...         # Cart + Catalog cache
    smtp_host: str = ...         # Notifications servisi
    cart_cache_ttl_seconds: int  # Cart servisi
```

Servisler birbirinin ayarlarını görüyor; ayrı yapılandırma imkânı yok.

---

## İhlal #8 — Servis Başına Health Check Yok (ORTA)

**`app/main.py:25-27`** — Tüm uygulama için tek endpoint:
```python
@app.get("/api/health")
def health() -> dict:
    return {"status": "ok"}
```

Tek endpoint hangi alt servisin (DB bağlantısı, Redis, SMTP) sorun yaşadığını söylemiyor. Kubernetes/Docker Compose readiness probe için yetersiz.

---

## İhlal #9 — Service Discovery Yok (ORTA)

**`app/config.py:13-15`** — Adresler hard-code:
```python
database_url: str = "postgresql+psycopg2://...@localhost:5432/storium_db"
redis_url: str = "redis://localhost:6379/1"
```

Birden fazla Catalog instance çalıştırılmak istendiğinde yönlendirme mekanizması yok.

---

## İhlal #10 — Blocking SMTP (ORTA)

**`app/services/notifications.py:42-59`** — Standart `smtplib` kullanımı:
```python
with smtplib.SMTP(settings.smtp_host, settings.smtp_port) as server:
    server.sendmail(...)   # ana thread'i bloklayan senkron çağrı
```

E-posta gönderimi süresince HTTP isteği yanıt veremiyor; timeout riski var.

---

## İhlal #11 — Circuit Breaker / Retry Yok (ORTA)

**`app/services/order_service.py:67-74`** — Hata durumunda yalnızca rollback:
```python
try:
    order = order_repo.order_create(...)
    catalog_repo.product_decrement_stock(...)
    self._db.commit()
except Exception:
    self._db.rollback()
    raise
```

Geçici hatalar (network timeout, DB bağlantı kopmasi) için yeniden deneme yok. Catalog servisi kısa süreliğine çevrimdışı olursa tüm checkout'lar başarısız olur.

---

## İhlal #12 — Paylaşılan Redis (ORTA)

**`app/services/cart_service.py:13`**
```python
CART_CACHE_KEY_PREFIX = "storium:cache:cart:"
```

**`app/services/catalog_service.py:20`**
```python
_CATEGORY_NAV_CACHE_KEY = "catalog:nav_tree:v1"
```

Her iki servis de aynı Redis instance'ına yazıyor. Catalog cache TTL ayarı yanlışsa Cart verileri etkilenebilir; izolasyon yok.

---

## Çapraz-İhlal Özet Tablosu

| İhlal | Şiddet | Çözen Faz |
|-------|--------|-----------|
| V1 — Paylaşılan DB | KRİTİK | Faz 2–4 |
| V2 — Çapraz import | KRİTİK | Faz 2–4 |
| V3 — Paylaşılan model | YÜKSEK | Faz 2–4 |
| V4 — API Gateway yok | YÜKSEK | Faz 1 |
| V5 — Senkron zincir | YÜKSEK | Faz 3 |
| V6 — Tek deploy | YÜKSEK | Faz 2–4 |
| V7 — Monolitik config | ORTA | Faz 2–4 |
| V8 — Health check yok | ORTA | Faz 5 |
| V9 — Service discovery | ORTA | Faz 1+5 |
| V10 — Blocking SMTP | ORTA | Faz 4 |
| V11 — Circuit breaker | ORTA | Faz 3+5 |
| V12 — Paylaşılan Redis | ORTA | Faz 2–3 |

## İlgili Belgeler

| Belge | Konu |
|-------|------|
| [20-phase0-1-infra-gateway.md](20-phase0-1-infra-gateway.md) | Faz 0 & 1: Altyapı + Traefik |
| [21-phase2-catalog-service.md](21-phase2-catalog-service.md) | Faz 2: Catalog servisi |
| [22-phase3-cart-orders.md](22-phase3-cart-orders.md) | Faz 3: Cart & Orders + event |
| [23-phase4-identity-notifications.md](23-phase4-identity-notifications.md) | Faz 4: Identity & Notifications |
| [24-phase5-observability.md](24-phase5-observability.md) | Faz 5: Gözlemlenebilirlik |
