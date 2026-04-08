# Architecture Decision Records (ADR)

Bu klasör, önemli mimari kararların **bağlam**, **karar** ve **sonuç** özetini tutar. Şablon: [0001-microservices-approach.md](0001-microservices-approach.md) başlık yapısı.

## İndeks

| ADR | Başlık | Durum |
|-----|--------|--------|
| [0001](0001-microservices-approach.md) | Hedef microservis yaklaşımı ve Strangler Fig | Kabul |
| [0002](0002-shared-library-boundaries.md) | Paylaşılan kütüphane sınırları | Taslak |

## Ne zaman ADR yazılır?

- Yeni mesaj broker seçimi, veri sahipliği değişikliği, kimlik modeli değişikliği gibi **geri dönüşü maliyetli** seçimler.
- Birden fazla takımı etkileyen API veya event şeması **breaking** değişikliği.

## İlgili belgeler

- [13-microservices-vision.md](../13-microservices-vision.md)
- [14-microservices-tech-stack.md](../14-microservices-tech-stack.md)
