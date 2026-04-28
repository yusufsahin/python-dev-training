# Teklif

Ürün spesifikasyonu: `urun-spesifikasyonu-v0.3.md`

## Web (React)

```bash
cd web
npm install
npm run dev
```

- **Stack:** Vite, React 19, Tailwind v4, shadcn/ui (Radix), Redux Toolkit, RTK Query, React Hook Form, Zod.
- **Tasarım sistemi:** `Designsystemcreation-main` ile hizalı tokenlar — `web/src/styles/theme.css`, `tw-animate-css`. Özet: `web/src/design-system/README.md`. Uygulamada **DS** sekmesinden önizleme.
- **API örnekleri:** `api/http/teklif-api.http`, `api/curl/cari.sh`, `api/curl/cari.ps1`
- **Ortam dosyaları:** `web/.env.example`, `web/.env.development`, `web/.env.staging`, `web/.env.production`

## API (FastAPI + PostgreSQL)

```bash
cd api-python
python -m venv .venv
.venv\Scripts\activate
pip install -e .
copy .env.example .env
alembic upgrade head
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Docker (UI + API + PostgreSQL)

```bash
cd .
docker compose up --build -d
```

- UI: `http://localhost:8080`
- API: `http://localhost:8001/health`
- UI üzerinden proxy API: `http://localhost:8080/api/health`

- **Ortam dosyaları:** `api-python/.env.example`, `api-python/.env.development`, `api-python/.env.staging`, `api-python/.env.production`
