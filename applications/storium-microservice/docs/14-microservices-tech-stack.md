# 14 — Microservis teknoloji yığını

Önerilen stack, [13-microservices-vision.md](13-microservices-vision.md) hedefleriyle uyumludur; kesin kütüphane seçimleri ADR ile sabitlenir ([adr/README.md](adr/README.md)).

## Özet yığın (sabitlenen seçimler)

| Katman | Teknoloji |
|--------|-----------|
| HTTP API | **FastAPI** |
| Veri erişimi | **SQLAlchemy 2** + **asyncpg** |
| Doğrulama ve şema | **Pydantic** (v2); FastAPI ile birlikte OpenAPI üretimi |
| Şema göçleri | **Alembic** (servis başına) |
| Ön yüz | **Next.js** (App Router) + **React**; genel durum için **React Context API** (kimlik, sepet, tema vb.) |

**Django kullanılmaz.** Backend bu Python yığınıdır (Python 3.12+).

## Backend (servis çatısı)

| Bileşen | Kullanım |
|---------|----------|
| **FastAPI** | HTTP servisleri; **OpenAPI 3** şeması; ASGI / async. |
| **Pydantic v2** | İstek/yanıt modelleri, ayarlar (`BaseSettings`), domain DTO’ları; OpenAPI ile hizalı tek kaynak. |
| **SQLAlchemy 2** + **asyncpg** | İlişkisel erişim; **database per service**; async session deseni. |
| **Alembic** | Servis başına bağımsız migrasyonlar. |

## Ön uç (React + Context API)

- **Next.js** + **React**: ürün listesi, sepet, sipariş, giriş akışları BFF/gateway üzerinden REST çağrıları ile beslenir; istemci bileşenlerinde `fetch` (ör. `NEXT_PUBLIC_API_BASE`).
- **Context API**: uygulama genelinde paylaşılan durum (ör. `AuthContext`, sepet kimliği, UI sayacı). Küçük/orta kapsam için yeterli; ileride çok sayıda bağımlı tüketici veya karmaşık async cache gerekiyorsa ayrı ADR ile Redux/Zustand vb. değerlendirilir.
- Derleme: **Next.js** (`next build`); Docker’da **standalone** çıktı; API tabanı URL’si build/runtime ortam değişkeni ile (gateway veya doğrudan servis).
- UI ayrı deploy birimi; backend yalnızca JSON API sunar (statik mount zorunlu değil).

## API ve sözleşme

- **OpenAPI 3** her servisin **source of truth**’u; şema repo’da veya artefact olarak versiyonlanır (süreç [18-api-contracts-testing-ops.md](18-api-contracts-testing-ops.md)).
- **Versiyonlama**: URL yolu (`/v1/...`) veya header; breaking değişiklik süreci 18’de tanımlıdır.

## Mesajlaşma (event bus)

| Seçenek | Ne zaman tercih |
|---------|------------------|
| **RabbitMQ** | Orta ölçek, klasik kuyruk/topik, operasyonel basitlik. |
| **Apache Kafka** | Yüksek hacim, uzun süreli log, çok tüketici, stream işleme. |

Seçim kriterleri: beklenen throughput, yeniden oynatma ihtiyacı, ekip deneyimi. Domain event tasarımı [15-microservices-data-and-events.md](15-microservices-data-and-events.md).

## Önbellek ve oturum

- **Redis**: sepet (`X-Cart-Id`), rate limit, kısa TTL cache; `REDIS_URL` ile yapılandırılır ([11-setup.md](11-setup.md)).
- Cart servisi için state **Redis veya** küçük ayrı DB; servis sınırı içinde kalır.

## API Gateway ve yerel edge

- **Docker Compose**: **Traefik** veya **nginx** ters vekil olarak yönlendirme, TLS sonlandırma (yerel sertifika), basit rate limit.
- **Kubernetes**: Ingress controller (ör. nginx, Traefik); üretim TLS ve rota kuralları [17-deployment-compose-and-k8s.md](17-deployment-compose-and-k8s.md).

## Kimlik ve güvenlik

- **OIDC / OAuth2**: harici IdP (Auth0, Keycloak, Azure AD vb.) veya self-hosted; kullanıcı akışı **token** tabanlı.
- **Servis-servis**: kısa ömürlü token, imzalı JWT veya mTLS (organizasyon politikasına göre); gateway arkasındaki iç ağda en azından **network policy** ve secret yönetimi.
- **Sırlar**: ortam değişkeni veya secret store; repoda asla düz metin ([17-deployment-compose-and-k8s.md](17-deployment-compose-and-k8s.md)).

## Gözlemlenebilirlik

- **OpenTelemetry**: trace export (OTLP); servisler arası **correlation-id** / trace-id yayılımı.
- **Metrik**: Prometheus uyumlu endpoint veya sidecar; Grafana panoları.
- **Log**: yapılandırılmış JSON; log seviyesi ve PII maskeleme [15-microservices-data-and-events.md](15-microservices-data-and-events.md) ile uyumlu.

## Dayanıklılık (servisler arası çağrı)

- **Timeout**: her çıkış çağrısında üst sınır (ör. 2–5 s aralığı servis kritikliğine göre); sınırsız bekleme yok.
- **Retry**: yalnızca **idempotent** işlemlerde ve sınırlı deneme + exponential backoff; POST/checkout için kör retry yok.
- **Circuit breaker**: downstream sürekli hata verdiğinde hızlı başarısız dönüş; cascade önleme.
- **Bulkhead**: thread pool / connection limit ile tek bağımlılığın tüm kapasiteyi tüketmesini sınırlama.

Bu maddeler uygulama kütüphanesinden bağımsız kavramsal zorunluluktur; implementasyon ADR veya servis şablonu ile seçilir.

## Paylaşılan kütüphane politikası (özet)

- İş mantığı paylaşımından kaçının; tekrarlayan ihtiyaçlar için önce **API genişletme** veya **event** değerlendirilir.
- İnce paylaşılan paketler (sabitler, küçük tip tanımları) ADR `0002` ile sınırlandırılabilir ([13-microservices-vision.md](13-microservices-vision.md)).

## İlgili belgeler

| Belge | Konu |
|-------|------|
| [15-microservices-data-and-events.md](15-microservices-data-and-events.md) | Veri, event, PII |
| [17-deployment-compose-and-k8s.md](17-deployment-compose-and-k8s.md) | Compose / K8s |
| [18-api-contracts-testing-ops.md](18-api-contracts-testing-ops.md) | Sözleşme ve SLO |
