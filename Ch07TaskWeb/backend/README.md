# Ch07TaskWeb Backend

FastAPI + SQLAlchemy + Pydantic + SQLite.

## Kurulum

```bash
pip install -r requirements.txt
```

## Çalıştırma

Proje kökünden (Ch07TaskWeb):

```bash
uvicorn app.main:app --reload --app-dir backend
```

Veya backend klasöründen:

```bash
cd backend
uvicorn app.main:app --reload
```

API dokümantasyonu: http://localhost:8000/docs

## Ortam

- `DATABASE_URL`: Varsayılan `sqlite:///./tasks.db`
