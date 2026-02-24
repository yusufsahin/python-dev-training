# Ch07TaskWeb – Görev Yöneticisi

FastAPI (backend) + React + TypeScript (frontend) ile tek sayfa görev yöneticisi.

## Yapı

- **backend/** – FastAPI, SQLAlchemy 2.x, Pydantic v2, SQLite
- **frontend/** – React 18, Vite, TypeScript, Tailwind, shadcn benzeri UI

## Docker ile yerel çalıştırma (önerilen)

```bash
cd Ch07TaskWeb
docker compose up -d
```

Uygulama: **http://localhost:8080**  
API doğrudan: `http://localhost:8080/api/` (nginx proxy)

Durdurmak: `docker compose down`  
Veritabanı kalıcı: `backend-data` volume kullanılır.

## Gereksinimler (Docker kullanmıyorsanız)

- Python 3.10+
- Node.js 18+

## Backend

```bash
cd Ch07TaskWeb
pip install -r backend/requirements.txt
uvicorn app.main:app --reload --app-dir backend
```

API: http://localhost:8000  
Dokümantasyon: http://localhost:8000/docs

Ortam (isteğe bağlı):

- `DATABASE_URL` – Varsayılan: `sqlite:///./tasks.db`

## Frontend

```bash
cd Ch07TaskWeb/frontend
npm install
npm run dev
```

Uygulama: http://localhost:5173

Geliştirmede Vite proxy `/api` isteklerini `http://localhost:8000` adresine yönlendirir. Production için `VITE_API_URL` ile tam API adresi verilebilir.

## Özellikler

- Görev CRUD (liste, filtre: durum, öncelik, kategori, arama)
- Kategori yönetimi (ekleme, silme)
- Tablo: Başlık, Öncelik, Durum, Son Tarih, Kategori (id gizli)
- Görev ekleme/düzenleme dialog’u, kategori yönetimi dialog’u
