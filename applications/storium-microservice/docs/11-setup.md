# 11 — Kurulum

## Gereksinimler

- Python 3.12+
- Node.js 20+ (sadece ön yüz geliştirme)
- PostgreSQL 16+ ve Redis 7 (yerel veya Docker)

## Ortam değişkenleri

`.env.example` dosyasını `.env` olarak kopyalayın. Önemli alanlar:

- `DATABASE_URL` — `postgresql+psycopg2://kullanıcı:parola@host:5432/veritabanı`
- `REDIS_URL` — örn. `redis://localhost:6379/1`
- `SECRET_KEY` — JWT imzası (üretimde güçlü rastgele)
- `CORS_ORIGINS` — virgülle ayrılmış liste (Next.js: `http://localhost:3000`)

## Yerel: backend

```powershell
cd applications/storium-microservice
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
# PostgreSQL + Redis ayakta; .env dolu olsun
alembic upgrade head
python -m app.seed
# İsteğe bağlı demo kullanıcı: $env:SEED_DEMO_USER="true"; python -m app.seed
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

API: `http://127.0.0.1:8000/api/health` — OpenAPI: `/docs`

## Yerel: frontend (ayrı terminal)

```powershell
cd frontend
npm install
npm run dev
```

`frontend/.env.local.example` dosyasından kopyalayın: `NEXT_PUBLIC_API_BASE` tarayıcıdan API taban URL’si (yerelde genelde `http://127.0.0.1:8000`).

## Docker (API + Next.js ayrı konteynerler)

```powershell
docker compose up --build
```

Varsayılan: UI `http://localhost:3000`, API `http://localhost:8001` (`NEXT_PUBLIC_API_BASE` build arg ile UI imajında).

Demo giriş (seed açıksa): kullanıcı `demo`, parola `storium-demo-2024`.

## Göçler

```powershell
alembic revision --autogenerate -m "açıklama"
alembic upgrade head
```
