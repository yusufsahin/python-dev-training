# 17 — Docker Compose ve Kubernetes özeti

Bu belge [11-setup.md](11-setup.md) yerel kurulumunu tamamlar; üretim kalıpları organizasyon politikasına göre sıkılaştırılır.

## Docker Compose (mevcut repo)

### Geliştirme (`docker-compose.yml`)

- Servisler: **db** (PostgreSQL), **redis**, **rabbitmq**, **traefik**, **api** (FastAPI), **ui** (Next.js standalone).
- Varsayılan portlar: UI **3000**, API doğrudan **8001**, Traefik (gateway) **9080**, Traefik dashboard **8080**, RabbitMQ yönetim **15672**, DB **5433** (host mapping, `.env` ile değişir).
- UI imajı build arg: **`NEXT_PUBLIC_API_BASE`** — tarayıcıdan kök URL; gateway kullanımında genelde `http://localhost:9080` (doğrudan API için `http://localhost:8001`).
- **Sırlar**: `.env` veya Compose `secrets`; repoda düz metin yok.

### Üretim (`docker-compose.prod.yml`)

- `docker compose --env-file .env.production -f docker-compose.prod.yml up -d --build` — değişkenler `environment` ile konteynıra aktarılır (ayrı `env_file` yolu gerekmez). Örnek: [.env.production.example](../.env.production.example).
- **WEB_PORT** / **UI_PORT** API ve Next’in host portları; **NEXT_PUBLIC_API_BASE** kullanıcı tarayıcısının göreceği API kökü (TLS ile tam URL önerilir).

### Gateway (isteğe bağlı yerel)

- **Traefik** veya **nginx** konteyneri ile `ui` + `api` tek host altında birleştirilebilir; üretimde TLS sonlandırma burada yapılır.

## Kubernetes (özet)

- **Deployment** + **Service** her mikroservis için; **Ingress** (nginx, Traefik, …) dış trafik.
- **ConfigMap** / **Secret** yapılandırma ve bağlantı dizeleri; **HorizontalPodAutoscaler** trafik eğrisine göre.
- **NetworkPolicy** iç doğrulama; veritabanı ve Redis yalnızca yetkili pod’lardan erişilebilir.
- Gözlemlenebilirlik: OTLP toplama, Prometheus scrape — bkz. [14-microservices-tech-stack.md](14-microservices-tech-stack.md).

## İlgili belgeler

| Belge | Konu |
|-------|------|
| [18-api-contracts-testing-ops.md](18-api-contracts-testing-ops.md) | CI/CD ve SLO |
| [11-setup.md](11-setup.md) | Geliştirici kurulumu |
