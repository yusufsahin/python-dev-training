# Storium — E-Commerce Modulith

## Proje Özeti
Storium modulith sürümü: tek deploy birimi içinde **modül sınırları** (`modules/*`) ve paylaşılan **çekirdek** (`core/`). Katmanlar: **Model → Repository → Service → DTO → View (Controller)**. Önbellek için **Redis** (`django-redis`); `REDIS_URL` yoksa geliştirme/test için **LocMem** kullanılır.

## Hızlı Başlangıç
PostgreSQL ayakta olmalı (yerelde kurulum veya `docker compose up -d` — bkz. `docker-compose.yml`). `.env` içinde `DB_*` değişkenlerini doldurun. Redis kullanmak için `REDIS_URL` tanımlayın (Docker Compose’ta otomatik: `redis://redis:6379/1`).

```bash
python -m venv .venv
source .venv/bin/activate           # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env                # SECRET_KEY ve DB_* değerlerini düzenle
python manage.py migrate
python manage.py seed_catalog          # örnek kategori/ürün (isteğe bağlı)
python manage.py createsuperuser
python manage.py runserver
```

## Temel Teknolojiler
| Katman       | Teknoloji                        |
|--------------|----------------------------------|
| Backend      | Python 3.12 / Django 5.x         |
| Frontend     | Bootstrap 5.3 (CDN)              |
| Veritabanı   | PostgreSQL (development + production) |
| Önbellek     | Redis + django-redis (veya LocMem) |
| E-posta      | Django Email + HTML Templates    |
| Statik dosya | WhiteNoise                       |
| Auth         | Django built-in auth             |

## Proje Yapısı (Özet)
```
storium/          ← Django proje paketi (settings, urls, wsgi)
modules/          ← Modüller (INSTALLED_APPS: modules.catalog, …)
  catalog/        ← Kategori ve ürün listesi/detay, arama
  cart/           ← Session tabanlı sepet (DB tablosu YOK)
  orders/         ← Sipariş oluşturma ve takibi
  notifications/  ← E-posta bildirim servisi
core/
  repositories/   ← Abstract Repository Protocol'leri + Django ORM impl.
  services/       ← Domain servis sınıfları (iş mantığı)
  dtos/           ← Dataclass tabanlı DTO'lar (Input / Output)
  exceptions/     ← Domain exception'ları
templates/        ← Proje geneli Django HTML templates
static/           ← CSS, JS, img
docs/             ← Tüm mimari ve gereksinim MD dosyaları
```

## Doküman Dizini
| Dosya                            | Konu                                  |
|----------------------------------|---------------------------------------|
| docs/01-architecture.md          | Klasör yapısı, katman sorumlulukları   |
| docs/02-models.md                | Tüm entity alan tanımları             |
| docs/03-repository-layer.md      | Repository protocol + implementasyon  |
| docs/04-service-layer.md         | Service metot imzaları + iş kuralları |
| docs/05-dto-layer.md             | Input / Output DTO sınıfları          |
| docs/06-catalog-module.md        | Katalog view, URL, template spec      |
| docs/07-cart-module.md           | Session sepet spec                    |
| docs/08-orders-module.md         | Sipariş akışı spec                    |
| docs/09-notifications-module.md  | E-posta bildirim spec                 |
| docs/10-ui-templates.md          | Bootstrap 5 template spec             |
| docs/11-setup.md                 | Kurulum, settings, env vars           |
| docs/12-modulith-redis.md        | Modulith düzeni + Redis önbellek      |

## Cursor Uygulama Sırası
Cursor aşağıdaki sırayı izleyerek uygulama geliştirmelidir:
1. `docs/11-setup.md` → Django projesi kur, requirements yükle
2. `docs/01-architecture.md` → Klasör/app yapısını oluştur
3. `docs/02-models.md` → Modeller + `makemigrations && migrate`
4. `docs/03-repository-layer.md` → `core/repositories/` implement et
5. `docs/05-dto-layer.md` → `core/dtos/` implement et
6. `docs/04-service-layer.md` → `core/services/` implement et
7. `docs/06-catalog-module.md` → Catalog app tamamla
8. `docs/07-cart-module.md` → Cart app tamamla
9. `docs/08-orders-module.md` → Orders app tamamla
10. `docs/09-notifications-module.md` → Notifications implement et
11. `docs/10-ui-templates.md` → Bootstrap 5 layout ve template'ler

## Mimari Prensipleri
- **View katmanı**: Sadece HTTP in/out. ORM sorgusu, e-posta gönderimi, iş mantığı YASAK.
- **Service katmanı**: Tüm iş mantığı burada. `@transaction.atomic` kullan.
- **Repository katmanı**: Sadece ORM sorguları. DTO bilmez, Model döner.
- **DTO katmanı**: **Pydantic v2** `BaseModel` (çıktılar `frozen=True`). ORM nesnesi içermez.
- **Model katmanı**: Alan tanımı + `__str__` + `Meta` + basit `@property`.
