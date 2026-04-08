# 16 — Microservis geçiş yol haritası

[13-microservices-vision.md](13-microservices-vision.md) Strangler Fig yaklaşımının fazlı özeti. Öncelik ve süre takım kapasitesine göre ADR ile revize edilir.

## Faz 0 — Ön koşullar

- OpenAPI şeması repo’da veya artefact olarak sabitlenir ([18-api-contracts-testing-ops.md](18-api-contracts-testing-ops.md)).
- Yerel ve CI’da sözleşme / smoke testleri çalışır.
- **Definition of Done (DoD)**: API değişiklikleri breaking olmadan veya sürüm yolu ile yayınlanır.

## Faz 1 — Edge ve yönlendirme

- API Gateway (veya ters vekil) ile dış tek giriş; mevcut monolit rotaları **proxy** ile korunur.
- **DoD**: İstemci (Next.js) yalnızca gateway URL’sine bağlanır; CORS ve TLS edge’de yönetilir ([17-deployment-compose-and-k8s.md](17-deployment-compose-and-k8s.md)).

## Faz 2 — İlk servis ayrıştırması (ör. Catalog)

- Catalog okuma/yazma ayrı deploy ve kendi DB’sine taşınır (veya mantıksal izolasyon).
- Monolit içinde kalan yollar kademeli kapatılır.
- **DoD**: Trafik ölçümü, hata oranı ve gecikme önceki seviyenin altında veya eşiğinde; geri dönüş planı dokümante.

## Faz 3 — Sepet ve sipariş

- Cart (Redis veya ayrı servis), Orders ayrı deploy; senkron zincirler kısaltılır, gerekli yerlerde event ([15-microservices-data-and-events.md](15-microservices-data-and-events.md)).
- **DoD**: Checkout uçtan uça testler; idempotent tüketici ve dead-letter stratejisi tanımlı.

## Faz 4 — Kimlik ve bildirim

- JWT yerine veya yanında OIDC ([14-microservices-tech-stack.md](14-microservices-tech-stack.md)); Notifications kuyruk tabanlı.
- **DoD**: Secret rotation, token ömrü ve servis-servis auth politikası yazılı.

## Riskler ve çıktılar

| Risk | Mitigasyon |
|------|------------|
| Dağıtık monolit | Sık iç çağrı yerine event ve aggregate API |
| Veri migrasyon hatası | Çift yazma, shadow read, kesme kontrol listesi |
| Operasyon yükü | Observability ve runbook ([18-api-contracts-testing-ops.md](18-api-contracts-testing-ops.md)) |

## İlgili belgeler

| Belge | Konu |
|-------|------|
| [17-deployment-compose-and-k8s.md](17-deployment-compose-and-k8s.md) | Ortamlar |
| [adr/0001-microservices-approach.md](adr/0001-microservices-approach.md) | Karar kaydı |
