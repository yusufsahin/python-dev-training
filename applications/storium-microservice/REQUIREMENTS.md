# Storium — E-ticaret (FastAPI + Next.js)

## Proje özeti

Tek deploy biriminde **FastAPI** REST API (`/api/...`), **PostgreSQL**, **Redis** (sepet + önbellek), **Next.js** (App Router) + **React** ön yüz (Context API). Kimlik: **JWT** (Bearer). Şema göçleri: **Alembic**.

## Hızlı başlangıç

PostgreSQL ve Redis ayakta olmalı. `.env.example` → `.env`.

```powershell
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
alembic upgrade head
python -m app.seed
# Demo kullanıcı: $env:SEED_DEMO_USER="true"; python -m app.seed
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Ön yüz (ayrı terminal): `cd frontend && npm install && npm run dev` — bkz. [docs/11-setup.md](docs/11-setup.md).

Docker: `docker compose up --build` → UI `http://localhost:3000`, API `http://localhost:8001` (ayrı servisler; bkz. `docker-compose.yml`).

## Teknolojiler

| Katman    | Teknoloji                          |
|-----------|-------------------------------------|
| API       | Python 3.12, FastAPI, Pydantic v2   |
| Veri      | SQLAlchemy 2, PostgreSQL, Alembic   |
| Önbellek  | Redis (sepet JSON + katalog nav; sepet TTL yapılandırılabilir) |
| Ön yüz    | Next.js 15 (App Router), React 19, Context API |
| Derleme   | Next.js (`next build`, standalone Docker)      |

## Dizin yapısı (özet)

```
app/              # FastAPI uygulaması
alembic/          # Veritabanı göçleri
frontend/         # Next.js (src/app/, public/)
docs/             # Mimari ve kurulum
```

## Doküman dizini

| Dosya | Konu |
|-------|------|
| [docs/01-architecture.md](docs/01-architecture.md) | Klasör ve katman özeti |
| [docs/11-setup.md](docs/11-setup.md) | Kurulum, Docker, göçler |
| [docs/13-microservices-vision.md](docs/13-microservices-vision.md) | Hedef microservis vizyonu |
| [docs/14-microservices-tech-stack.md](docs/14-microservices-tech-stack.md) | Stack ve dayanıklılık |
| [docs/15-microservices-data-and-events.md](docs/15-microservices-data-and-events.md) | Veri, event, PII |
| [docs/16-migration-roadmap.md](docs/16-migration-roadmap.md) | Geçiş fazları ve DoD |
| [docs/17-deployment-compose-and-k8s.md](docs/17-deployment-compose-and-k8s.md) | Compose ve K8s özeti |
| [docs/18-api-contracts-testing-ops.md](docs/18-api-contracts-testing-ops.md) | Sözleşme, test, SLO |
| [docs/19-violation-analysis.md](docs/19-violation-analysis.md) | Monolit / microservis ihlal analizi |
| [docs/20-phase0-1-infra-gateway.md](docs/20-phase0-1-infra-gateway.md) | Faz 0–1: kontrat, smoke, Traefik |
| [docs/21-phase2-catalog-service.md](docs/21-phase2-catalog-service.md) | Faz 2: Catalog servisi |
| [docs/22-phase3-cart-orders.md](docs/22-phase3-cart-orders.md) | Faz 3: Cart ve Orders |
| [docs/23-phase4-identity-notifications.md](docs/23-phase4-identity-notifications.md) | Faz 4: Identity ve bildirimler |
| [docs/24-phase5-observability.md](docs/24-phase5-observability.md) | Faz 5: gözlemlenebilirlik |
| [docs/adr/README.md](docs/adr/README.md) | Mimari karar kayıtları (ADR) |

Smoke testler: `pip install -r requirements-dev.txt` ve `pytest tests/smoke -v` (veya `make test-smoke`). OpenAPI dondurma: `python scripts/export_openapi.py` veya `make openapi`.

## Mimari ilkeler

- **Router**: HTTP ve doğrulama; iş mantığı yalnızca `app/services/` içinde (gelecekte `services/<bounded>/`).
- **Repository**: SQLAlchemy sorguları; servisler repo fonksiyonlarını kullanır.
- **Şemalar**: `schemas/` (Pydantic) API sözleşmesi ile uyumlu.

Hedef microservis ayrıştırması için [docs/13-microservices-vision.md](docs/13-microservices-vision.md) bölümüne bakın.
