# 12 — Modulith ve Redis önbellek

## Modulith ne demek?

Bu depo **tek süreç / tek deploy** kalır; monolith’ten farkı, Django uygulamalarının `apps/` yerine **`modules/`** altında toplanması ve `core/` ile modüller arasında net bir ayrımın dokümante edilmesidir. Modüller birbirinin içine doğrudan “iş mantığı” sızmamalı; ortak iş kuralları `core/services` ve repository protokolleri üzerinden gider.

- **Paket yolu**: `modules.catalog`, `modules.cart`, … (`INSTALLED_APPS` ve `include("modules…")`).
- **Migration etiketi**: Django uygulama etiketi (`catalog`, `cart`, …) değişmediği için mevcut migration dosyaları aynı kalır.

## Redis ve Django cache

- Ortam değişkeni **`REDIS_URL`** (ör. `redis://localhost:6379/1` veya Docker’da `redis://redis:6379/1`) tanımlıysa `CACHES["default"]` **django-redis** ile Redis’e bağlanır.
- `REDIS_URL` boşsa **`LocMemCache`** kullanılır (yerel `runserver`, tek worker).
- `python manage.py test` çalışırken **`DummyCache`** seçilir; böylece LocMem’in testler arasında taşınması önlenir.

`docker-compose.yml` içinde `redis` servisi ve `web` için `REDIS_URL` tanımlıdır.

## Nerede kullanılıyor?

- **`CatalogService.get_category_nav_tree()`**: Kategori navigasyon ağacı 300 sn TTL ile önbelleğe alınır (her istekte tekrarlanan sorguları azaltır).
- **`invalidate_category_nav_cache()`**: `seed_catalog` komutu ve **Category** admin kayıt/silme işlemlerinden sonra çağrılarak menü önbelleği temizlenir.

İleride benzer anahtarlarla ürün listesi veya öne çıkan ürünler de cache’lenebilir; anahtar sürümü veya TTL ile geçerlilik yönetilir.
