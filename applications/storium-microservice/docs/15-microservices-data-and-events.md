# 15 — Veri sahipliği, event’ler ve PII

Bu belge [13-microservices-vision.md](13-microservices-vision.md) ve [14-microservices-tech-stack.md](14-microservices-tech-stack.md) ile tutarlıdır; servis sınırları kesinleştikçe ADR ile güncellenir.

## Database per service

- Her bounded context **kendi** ilişkisel şemasına (veya Redis gibi kendi state deposuna) sahiptir.
- Başka servisin tablolarına **doğrudan** bağlantı yok; ihtiyaç **API** veya **event** ile karşılanır.
- Geçiş döneminde tek PostgreSQL örneği üzerinde **mantıksal** ayrım (şema veya ayrı DB) mümkündür; fiziksel paylaşım geçicidir.

## Tutarlılık

- **Senkron yol**: kullanıcı isteği boyunca HTTP + transaction (ör. sipariş oluşturma anı).
- **Asenkron yol**: bildirim, arama indeksi, rapor; **eventual consistency** ve idempotent tüketici.

## Outbox ve saga (taslak)

- **Transactional outbox**: aynı DB transaction içinde iş kaydı + “gönderilecek event” satırı; ayrı işleyici broker’a yazar — mesaj kaybını önler.
- **Saga / orchestration**: uzun süren çok adımlı süreçlerde her adım geri alınabilir veya telafi edici iş (compensation) tanımlanır; ör. stok düşümü + ödeme + bildirim.

## Örnek domain event’ler (isimlendirme)

| Event | Üreten bağlam | Tipik tüketiciler |
|-------|----------------|-------------------|
| `OrderPlaced` | Orders | Notifications, Analytics |
| `StockReserved` | Catalog / Inventory | Orders |
| `PaymentCaptured` | Payments (gelecek) | Orders, Notifications |

Olay şeması (JSON Schema veya Avro) versiyonlanır; geriye dönük uyumluluk kuralları [18-api-contracts-testing-ops.md](18-api-contracts-testing-ops.md) ile hizalanır.

## PII ve loglama

- Log ve trace içinde **e-posta, telefon, tam adres** gibi alanlar maskelenir veya hash’lenir; ham PII yalnızca yetkili servislerde ve kısa retention ile tutulur.
- GDPR/ KVKK kapsamında silme talepleri **sahip servis** üzerinden orkestre edilir; event log’larında PII taşımaktan kaçınılır veya TTL uygulanır.

## İlgili belgeler

| Belge | Konu |
|-------|------|
| [16-migration-roadmap.md](16-migration-roadmap.md) | Veri kesme fazları |
| [18-api-contracts-testing-ops.md](18-api-contracts-testing-ops.md) | Şema ve test |
