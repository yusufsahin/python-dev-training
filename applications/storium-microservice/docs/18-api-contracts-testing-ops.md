# 18 — API sözleşmeleri, test ve operasyon

OpenAPI üretimi FastAPI ile otomatik (`/docs`, `/openapi.json`). Bu belge süreç ve kalite çubuğunu tanımlar.

## Sözleşme (contract)

- **Kaynak**: servis repo’sundaki OpenAPI şeması veya yayınlanan artefact (semver).
- **Breaking değişiklik**: zorunlu alan kaldırma, tip daraltma, hata kodu anlam değişikliği — **major** veya yeni yol (`/v2`).
- **Tüketici uyumu**: Next.js veya BFF için isteğe bağlı **codegen** veya manuel DTO; şema diff’i PR’da gözden geçirilir.

## Test

- **Contract test**: tüketici beklediği şema ile üretilen şemayı karşılaştırır (Schemathesis, Dredd, veya özel).
- **Smoke**: `/api/health`, kritik okuma yolları (catalog, cart) deploy sonrası.
- **Yük / performans**: hedef p95 gecikme ve hata oranı eşikleri takımın SLO’suna bağlanır.

## Operasyon ve SLO

- **SLO örnekleri**: API kullanılabilirlik %99.5 (aylık); p95 okuma süresi 500 ms altı (yerel ağ içi, hedef).
- **Hata bütçesi** tükendiğinde yeni özellik yerine güvenilirlik çalışması öncelenir.
- **Runbook**: veritabanı kesintisi, Redis kesintisi, yoğun trafik — kısa adımlar ve iletişim kanalı.

## İlgili belgeler

| Belge | Konu |
|-------|------|
| [14-microservices-tech-stack.md](14-microservices-tech-stack.md) | Dayanıklılık desenleri |
| [adr/README.md](adr/README.md) | Mimari karar indeksi |
