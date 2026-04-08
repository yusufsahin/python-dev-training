# 01 — Uygulama yapısı (FastAPI + React)

## Genel

- **Backend**: `app/` paketi — FastAPI, SQLAlchemy, Pydantic.
- **Ön yüz**: `frontend/` — **Next.js** (App Router), React, durum için **Context API**.
- **Veri**: PostgreSQL (Alembic göçleri `alembic/versions/`).
- **Sepet**: Yalnızca **Redis önbelleği** (`storium:cache:cart:{cart_id}`), JSON; `X-Cart-Id` ile istemci UUID’si. TTL: `CART_CACHE_TTL_SECONDS` (varsayılan 30 gün; her okumada süre yenilenir).

## Backend dizinleri

```
app/
  main.py           # FastAPI uygulaması, CORS, router’lar (UI ayrı Next.js servisi)
  config.py         # Ayarlar (pydantic-settings)
  database.py       # Engine + SessionLocal
  models.py         # SQLAlchemy modelleri
  seed.py           # Örnek veri
  routers/          # HTTP: auth, catalog, cart, orders
  services/         # İş mantığı
  repositories/   # Sorgu yardımcıları
  schemas/        # Pydantic şemaları (API / DTO)
  exceptions.py
  security.py       # JWT, parola hash
```

## API öneki

Tüm JSON API’ler `/api` altında (ör. `/api/catalog/featured`, `/api/auth/login`).

## İlgili belgeler

- [11-setup.md](11-setup.md) — yerel kurulum ve Docker
- [13-microservices-vision.md](13-microservices-vision.md) — hedef servis sınırları
- [14-microservices-tech-stack.md](14-microservices-tech-stack.md) — teknoloji yığını
