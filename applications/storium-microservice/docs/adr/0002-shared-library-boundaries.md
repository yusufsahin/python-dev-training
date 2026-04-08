# ADR 0002: Paylaşılan kütüphane sınırları

## Durum

Taslak

## Bağlam

Birden fazla serviste tekrarlayan kod, “ortak paket” ile paylaşılmak istenebilir. Aşırı paylaşım **dağıtık monolit** ve sürüm kilidine yol açar ([13-microservices-vision.md](../13-microservices-vision.md)).

## Karar (taslak)

- **İzinli**: ince, stabil yapılar — correlation ID sabitleri, ortak hata gövdesi JSON şeması, JWT claim isimleri (yalnızca string sabitler).
- **Kaçınılacak**: domain kuralları, repository implementasyonları, büyük “ortak DTO” paketleri; tercih **açık HTTP API** ve **versiyonlu event şeması**.

## Sonuçlar

Paylaşım ihtiyacı arttığında önce API veya event ile sınırlandırma değerlendirilir; paket çıkarma son çare olarak ADR ile onaylanır.

## İlgili belgeler

- [14-microservices-tech-stack.md](../14-microservices-tech-stack.md) — “Paylaşılan kütüphane politikası”
