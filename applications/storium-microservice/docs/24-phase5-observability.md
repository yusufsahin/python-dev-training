# 24 — Faz 5: Gözlemlenebilirlik, sağlık ve keşif

Bu belge [19-violation-analysis.md](19-violation-analysis.md) içindeki şu ihlalleri hedefler: **V8** (servis başına health), **V9** (service discovery — dokümante operasyon modeli), **V11** (dayanıklılık gözlemi ve gateway ile birlikte).

Önceki faz: [23-phase4-identity-notifications.md](23-phase4-identity-notifications.md)

[14-microservices-tech-stack.md](14-microservices-tech-stack.md) bölümleriyle hizalı: OpenTelemetry, yapılandırılmış log, metrik.

---

## 5.1 Health ve readiness (V8)

Monolitteki tek uç ([app/main.py](../app/main.py) `/api/health`) yerine **her serviste** ayrı kontroller:

| Endpoint | Amaç | Örnek kontroller |
|----------|------|------------------|
| `GET /health` (liveness) | Süreç yaşıyor mu | 200 sabit |
| `GET /ready` (readiness) | Trafiği kabul edebilir mi | DB ping, Redis ping, broker ping |

Kubernetes örneği:

```yaml
readinessProbe:
  httpGet:
    path: /ready
    port: 8000
  initialDelaySeconds: 10
  periodSeconds: 5
```

Docker Compose `healthcheck` aynı `/ready` yolunu kullanabilir.

---

## 5.2 Service discovery (V9)

**Hedef model (bu repo ile uyumlu):**

- **Docker:** Traefik Docker provider — konteyner label’ları ile dinamik rota; yeni replika eklendiğinde manuel DNS güncellemesi gerekmez.
- **Kubernetes:** Ingress controller + `Service` DNS (`catalog.storium.svc.cluster.local`); isteğe bağlı **CoreDNS** ve harici trafik için Ingress host kuralları.

İsteğe bağlı: **Consul** / **Linkerd** gibi mesh — ekip büyüklüğüne göre ADR.

Statik `localhost` URL’leri yalnızca geliştirme içindir; üretimde gateway veya internal DNS kullanılır.

---

## 5.3 OpenTelemetry ve log (V8, V11 ile ilişkili)

- **Trace:** Her servis OTLP exporter; ingress → servis → outbound HTTP span’leri.
- **Correlation:** `X-Request-Id` veya W3C `traceparent` header’larının gateway’den geçirilmesi.
- **Log:** JSON satır log; PII maskeleme ([15-microservices-data-and-events.md](15-microservices-data-and-events.md)).
- **Metrik:** HTTP istek sayısı, latency histogram, kuyruk derinliği, SMTP hata oranı.

**V11:** Circuit breaker açıldığında metrik alarmı (ör. Prometheus alert); retry storm’larını log/trace ile tespit.

---

## 5.4 Dashboard ve runbook

- Grafana panoları: servis başına RED (Rate, Errors, Duration) ve bağımlılık özeti.
- Runbook: “Catalog ready başarısız”, “RabbitMQ tüketici geride”, “SMTP DLQ birikiyor” — kısa adımlar ([18-api-contracts-testing-ops.md](18-api-contracts-testing-ops.md)).

---

## DoD — Faz 5

- [ ] Tüm mikroservislerde `/ready` bağımlılıkları doğruluyor (V8).
- [ ] Traefik veya K8s Ingress ile dış trafik tek girişten servis keşfine bağlı (V9 operasyonel).
- [ ] OTLP ile trace toplanıyor; en az bir örnek dashboard canlı.
- [ ] Correlation-id uçtan uca görünüyor (log veya trace UI’da doğrulandı).

---

## Geçiş özeti

[19-violation-analysis.md](19-violation-analysis.md) tablosundaki ihlaller, Faz 0–5 ile **hedeflenen** teknik borç azaltımına karşılık gelir. Tüm fazların tamamlanması, monolitin Traefik üzerinden **tamamen devre dışı** kalması ve her bounded context’in kendi deploy + veri sınırına sahip olması ile sonuçlanır.

## İlgili belgeler

| Belge | Konu |
|-------|------|
| [19-violation-analysis.md](19-violation-analysis.md) | İhlal listesi ve faz eşlemesi |
| [20-phase0-1-infra-gateway.md](20-phase0-1-infra-gateway.md) | Gateway temeli |
| [17-deployment-compose-and-k8s.md](17-deployment-compose-and-k8s.md) | Compose / K8s |
