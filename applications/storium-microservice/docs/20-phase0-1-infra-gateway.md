# 20 — Faz 0 & 1: Altyapı Temeli ve API Gateway

Bu belge [19-violation-analysis.md](19-violation-analysis.md) — V4, V9 ihlallerini çözer.  
Mevcut monolite **dokunulmaz**; yeni altyapı katmanı eklenir.

---

## Faz 0 — Ön Koşullar

### 0.1 Dizin Yapısı

Proje kökünde oluşturulacak yeni dizinler:

```
storium-microservice/
├── services/               ← her mikroservis buraya taşınacak
│   ├── catalog/
│   ├── cart/
│   ├── orders/
│   ├── identity/
│   └── notifications/
├── infra/
│   ├── gateway/            ← Traefik konfigürasyonu
│   ├── shared/             ← paylaşılan docker-compose parçaları
│   └── contracts/          ← dondurulmuş OpenAPI şeması
└── tests/
    └── smoke/              ← mevcut endpoint'ler için smoke testleri
```

**Bash komutu (bir kere çalıştır):**
```bash
mkdir -p services/{catalog,cart,orders,identity,notifications} \
         infra/{gateway,shared,contracts} \
         tests/smoke
```

---

### 0.2 OpenAPI Kontrat Dondurma

Mevcut monoliti kırmadan önce tüm endpoint şemasını kayıt altına al.

**`scripts/export_openapi.py`** (yeni dosya):
```python
"""
OpenAPI kontratını infra/contracts/openapi.json olarak dondurur.
Çalıştırma: python scripts/export_openapi.py
"""
import json, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from app.main import app

output = Path(__file__).parent.parent / "infra/contracts/openapi.json"
output.parent.mkdir(parents=True, exist_ok=True)
output.write_text(json.dumps(app.openapi(), indent=2, ensure_ascii=False))
print(f"Donduruldu: {output}")
```

**Çalıştırma (bağımlılıklar kuruluyken):**
```bash
python scripts/export_openapi.py
```

`infra/contracts/openapi.json` dosyası oluşur; bunu git'e commit et.  
İleride bir endpoint silinirse veya tipi değişirse CI bu dosyaya kıyasla uyarı verir.

---

### 0.3 Smoke Testleri

**`tests/smoke/conftest.py`**:
```python
import pytest
from httpx import AsyncClient
from app.main import app

@pytest.fixture
async def client():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac
```

**`tests/smoke/test_health.py`**:
```python
import pytest

@pytest.mark.anyio
async def test_health(client):
    r = await client.get("/api/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"
```

**`tests/smoke/test_catalog_endpoints.py`**:
```python
import pytest

@pytest.mark.anyio
async def test_featured_products(client):
    r = await client.get("/api/catalog/featured")
    assert r.status_code == 200
    assert isinstance(r.json(), list)

@pytest.mark.anyio
async def test_catalog_nav(client):
    r = await client.get("/api/catalog/nav")
    assert r.status_code == 200

@pytest.mark.anyio
async def test_catalog_search_empty_query_rejected(client):
    r = await client.get("/api/catalog/search?q=")
    assert r.status_code == 422  # Pydantic doğrulama hatası

@pytest.mark.anyio
async def test_catalog_search_valid(client):
    r = await client.get("/api/catalog/search?q=test")
    assert r.status_code == 200
```

**`tests/smoke/test_auth_endpoints.py`**:
```python
import pytest

@pytest.mark.anyio
async def test_register_validation(client):
    r = await client.post("/api/auth/register", json={})
    assert r.status_code == 422

@pytest.mark.anyio
async def test_login_wrong_credentials(client):
    r = await client.post(
        "/api/auth/login",
        data={"username": "nobody@test.com", "password": "wrong"},
    )
    assert r.status_code in (401, 422)

@pytest.mark.anyio
async def test_me_unauthenticated(client):
    r = await client.get("/api/auth/me")
    assert r.status_code == 401
```

**`tests/smoke/test_cart_endpoints.py`**:
```python
import pytest

@pytest.mark.anyio
async def test_get_cart_no_header(client):
    # X-Cart-Id header'ı olmadan boş sepet beklenir
    r = await client.get("/api/cart")
    assert r.status_code == 200

@pytest.mark.anyio
async def test_add_to_cart_unauthenticated(client):
    r = await client.post("/api/cart/items", json={"product_id": 1, "quantity": 1})
    assert r.status_code in (200, 400, 401, 404)  # smoke: çökmemeli
```

**`tests/smoke/test_orders_endpoints.py`**:
```python
import pytest

@pytest.mark.anyio
async def test_checkout_unauthenticated(client):
    r = await client.post("/api/orders/checkout", json={})
    assert r.status_code == 401

@pytest.mark.anyio
async def test_list_orders_unauthenticated(client):
    r = await client.get("/api/orders")
    assert r.status_code == 401
```

**`pytest.ini`** (yoksa ekle):
```ini
[pytest]
asyncio_mode = auto
```

**Gerekli ek paket:**
```
httpx>=0.27
anyio[trio]>=4
pytest-anyio>=0.0.0
```

---

### 0.4 RabbitMQ Altyapısı

**`infra/shared/docker-compose.infra.yml`** (yeni dosya):
```yaml
# Paylaşılan altyapı: DB'ler, Redis, RabbitMQ
# Kullanım: docker compose -f infra/shared/docker-compose.infra.yml up -d
services:
  rabbitmq:
    image: rabbitmq:3.13-management-alpine
    ports:
      - "5672:5672"   # AMQP
      - "15672:15672" # Yönetim paneli: http://localhost:15672 (guest/guest)
    environment:
      RABBITMQ_DEFAULT_USER: storium
      RABBITMQ_DEFAULT_PASS: storium_pass
    healthcheck:
      test: ["CMD", "rabbitmq-diagnostics", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5
    volumes:
      - rabbitmq_data:/var/lib/rabbitmq

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 5s
      timeout: 3s
      retries: 5

volumes:
  rabbitmq_data:
```

**DoD Faz 0:**
- [ ] `infra/contracts/openapi.json` commit edildi
- [ ] `pytest tests/smoke/` — tüm testler geçiyor (DB mock veya test DB ile)
- [ ] `docker compose -f infra/shared/docker-compose.infra.yml up -d` — RabbitMQ ayakta

---

## Faz 1 — API Gateway (Traefik)

**Çözdüğü ihlaller:** V4 (API Gateway yok), V9 (service discovery yok)

### 1.1 Traefik Statik Konfigürasyon

**`infra/gateway/traefik.yml`** (yeni dosya):
```yaml
# Traefik statik konfigürasyonu
api:
  dashboard: true   # http://localhost:8080/dashboard/

entryPoints:
  web:
    address: ":80"

providers:
  docker:
    exposedByDefault: false
    network: storium_net

log:
  level: INFO

accessLog: {}
```

### 1.2 docker-compose.yml Güncellemesi

Mevcut `docker-compose.yml` dosyasını aşağıdaki gibi güncelle.  
**Değişiklikler:**
1. `traefik` servisi eklendi
2. `api` servisine Traefik label'ları eklendi
3. `ui` servisi gateway üzerinden erişim için güncellendi
4. `storium_net` ağı eklendi

```yaml
# Tam yığın: UI http://localhost:3000 | API Gateway http://localhost:9080 (host) -> Traefik :80
# PostgreSQL: localhost:5433 | Redis: 6379 | RabbitMQ: 5672
services:

  # ── Altyapı ──────────────────────────────────────────────────────────────
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    networks:
      - storium_net
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 5s
      timeout: 3s
      retries: 5

  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_USER: storium_user
      POSTGRES_PASSWORD: storium_password
      POSTGRES_DB: storium_db
    ports:
      - "${DOCKER_DB_PORT:-5433}:5432"
    networks:
      - storium_net
    volumes:
      - storium_pgdata:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U storium_user -d storium_db"]
      interval: 5s
      timeout: 5s
      retries: 5

  rabbitmq:
    image: rabbitmq:3.13-management-alpine
    ports:
      - "5672:5672"
      - "15672:15672"
    networks:
      - storium_net
    environment:
      RABBITMQ_DEFAULT_USER: storium
      RABBITMQ_DEFAULT_PASS: storium_pass
    healthcheck:
      test: ["CMD", "rabbitmq-diagnostics", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5
    volumes:
      - rabbitmq_data:/var/lib/rabbitmq

  # ── API Gateway (Traefik) ─────────────────────────────────────────────────
  traefik:
    image: traefik:v3.0
    command:
      - "--api.dashboard=true"
      - "--api.insecure=true"          # Dashboard: http://localhost:8080
      - "--providers.docker=true"
      - "--providers.docker.exposedByDefault=false"
      - "--providers.docker.network=storium_net"
      - "--entrypoints.web.address=:80"
    ports:
      - "${DOCKER_GATEWAY_WEB_PORT:-9080}:80"   # API gateway (host:container)
      - "${DOCKER_TRAEFIK_UI_PORT:-8080}:8080"  # Traefik dashboard
    networks:
      - storium_net
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock:ro
    restart: unless-stopped

  # ── Monolit API (geçici — Strangler Fig: kademeli kapatılacak) ────────────
  api:
    build: .
    command: >
      uvicorn app.main:app
      --host 0.0.0.0
      --port 8000
    networks:
      - storium_net
    environment:
      SECRET_KEY: ${SECRET_KEY:-docker-local-dev-change-me}
      DATABASE_URL: postgresql+psycopg2://storium_user:storium_password@db:5432/storium_db
      DB_NAME: storium_db
      DB_USER: storium_user
      DB_PASSWORD: storium_password
      DB_HOST: db
      DB_PORT: "5432"
      REDIS_URL: redis://redis:6379/1
      RUN_SEED: "true"
      SEED_DEMO_USER: "true"
      CORS_ORIGINS: "http://localhost:3000,http://127.0.0.1:3000,http://localhost:9080,http://127.0.0.1:9080,http://localhost:8001,http://127.0.0.1:8001"
    restart: unless-stopped
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_healthy
    healthcheck:
      test:
        [
          "CMD", "python", "-c",
          "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/api/health', timeout=5)",
        ]
      interval: 15s
      timeout: 10s
      retries: 5
      start_period: 90s
    labels:
      # Traefik: /api/* isteklerini monolit API'ye yönlendir
      - "traefik.enable=true"
      - "traefik.http.routers.api-monolith.rule=PathPrefix(`/api`)"
      - "traefik.http.routers.api-monolith.entrypoints=web"
      - "traefik.http.services.api-monolith.loadbalancer.server.port=8000"
      # Öncelik: yeni mikroservis router'ları daha yüksek priority almalı
      - "traefik.http.routers.api-monolith.priority=1"

  # ── Frontend ─────────────────────────────────────────────────────────────
  ui:
    build:
      context: ./frontend
      dockerfile: Dockerfile
      args:
        # Frontend artık gateway üzerinden erişiyor (doğrudan API port yok)
        NEXT_PUBLIC_API_BASE: http://localhost:${DOCKER_GATEWAY_WEB_PORT:-9080}
    ports:
      - "${DOCKER_UI_PORT:-3000}:3000"
    networks:
      - storium_net
    depends_on:
      api:
        condition: service_healthy
    restart: unless-stopped

networks:
  storium_net:
    driver: bridge

volumes:
  storium_pgdata:
  rabbitmq_data:
```

### 1.3 Frontend API Base Güncelleme

**`frontend/src/lib/api.js`** — `NEXT_PUBLIC_API_BASE` değişkenini runtime'dan oku (zaten yapılmış), sadece `.env.local` şablonunu güncelle:

**`frontend/.env.local.example`** (oluştur veya güncelle):
```env
# Geliştirmede doğrudan API (docker-compose olmadan):
# NEXT_PUBLIC_API_BASE=http://127.0.0.1:8000

# Docker Compose ile (Traefik gateway üzerinden; varsayılan host portu 9080):
NEXT_PUBLIC_API_BASE=http://localhost:9080
```

### 1.4 Doğrulama

Kök `docker-compose.yml` içinde Traefik **web** girişi varsayılan olarak host **9080** portuna map edilir (`DOCKER_GATEWAY_WEB_PORT`). Dashboard **8080**’dedir.

```bash
# Tam yığın veya en azından traefik + api + db + redis
docker compose up -d

# Gateway üzerinden health check
curl http://localhost:9080/api/health
# Beklenen: {"status":"ok"}

# Traefik dashboard
open http://localhost:8080/dashboard/

# Frontend artık gateway üzerinden erişmeli
curl http://localhost:9080/api/catalog/featured
```

**DoD Faz 1:**
- [ ] `curl http://localhost:9080/api/health` → `{"status":"ok"}`
- [ ] Traefik dashboard'da `api-monolith` router görünüyor
- [ ] Frontend `NEXT_PUBLIC_API_BASE=http://localhost:9080` ile çalışıyor
- [ ] Eski doğrudan port erişimi (`localhost:8001`) hâlâ çalışıyor (geriye dönük uyumluluk)

---

## Sonraki Adım

Faz 1 tamamlandıktan sonra → [21-phase2-catalog-service.md](21-phase2-catalog-service.md)
