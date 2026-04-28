# Teklif API (FastAPI)

Bu servis, `cariler` ve `urunler` endpointlerini mevcut UI ile uyumlu tutar ve `teklifler` domainini ekler.

## Mimari

- `app/domain`: Entity, enum ve repository portları
- `app/application`: Use-case/service katmanı
- `app/infrastructure`: SQLAlchemy adapterları, DB session, seed
- `app/interfaces/http`: FastAPI router ve Pydantic şemaları
- `app/bootstrap`: Port-adapter bağlama (container)

## Kurulum

```bash
cd api-python
python -m venv .venv
.venv\Scripts\activate
pip install -e .
```

## Çalıştırma

```bash
cd api-python
copy .env.development .env
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Ortam stratejisi

- Lokal geliştirme: `.env.development`
- Staging: `.env.staging`
- Production: `.env.production`
- Uygulama her zaman `.env` dosyasını okur; hedef ortama göre ilgili dosyayı `.env` olarak kopyalayın.

## Migration

```bash
cd api-python
alembic upgrade head
```

## Docker Compose

```bash
cd api-python
copy .env.example .env
docker compose up --build
```
