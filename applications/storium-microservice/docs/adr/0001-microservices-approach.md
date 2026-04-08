# ADR 0001: Hedef microservis yaklaşımı (Strangler Fig)

## Durum

Kabul (eğitim / referans repo bağlamında)

## Bağlam

Storium başlangıçta modüler monolit (FastAPI, tek PostgreSQL, Redis sepet, Next.js UI) olarak geliştirilmektedir. Uzun vadede bounded context başına ayrı deploy ve **database per service** hedeflenmektedir.

## Karar

- Geçiş **Strangler Fig** ile yapılır: trafik gateway üzerinden kademeli olarak yeni servislere yönlendirilir.
- Senkron iletişimde **OpenAPI** uyumlu REST; asenkron yan etkilerde **domain event** ve mesaj altyapısı (RabbitMQ veya Kafka — ayrı ADR).
- Ön yüz **Next.js**; edge’de API Gateway veya BFF kullanımına izin verilir.

## Sonuçlar

**Olumlu**: Bağımsız ölçekleme, takım sınırları ile kod hizalaması, teknoloji yükseltmelerinin servis bazlı yapılması.

**Olumsuz / maliyet**: Dağıtık sistem karmaşıklığı, tutarlılık ve gözlemlenebilirlik gereksinimleri; operasyon yükü artar.

## İlgili belgeler

- [13-microservices-vision.md](../13-microservices-vision.md)
- [16-migration-roadmap.md](../16-migration-roadmap.md)
