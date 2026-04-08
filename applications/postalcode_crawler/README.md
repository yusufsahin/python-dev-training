# PTT posta kodu — Scrapy

Türkiye PTT resmi sitesindeki [Posta Kodu Sorgulama](https://www.ptt.gov.tr/posta-kodu) sayfasının kullandığı HTTP API’yi çağırarak il → ilçe → sokak/mahalle düzeyinde posta kodlarını toplar ve CSV veya JSON Lines olarak kaydeder.

## Kurulum

Python 3.10+ önerilir (Scrapy sürümünüze göre değişebilir).

```powershell
cd applications\postalcode_crawler
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Çalıştırma

Tam tarama binlerce `POST` isteği üretir; `settings.py` içindeki `DOWNLOAD_DELAY` ile siteye yük bindirmemek için bir gecikme vardır. Tam koşu uzun sürebilir.

```powershell
scrapy crawl ptt_posta_kodu -o posta_kodlari.jsonl
```

veya CSV:

```powershell
scrapy crawl ptt_posta_kodu -o posta_kodlari.csv
```

### Hızlı deneme (kısıtlı tarama)

Paralel kuyruk yüzünden `CLOSESPIDER_ITEMCOUNT` tek başına beklenenden fazla satır yazdırabilir. Küçük deneme için örümcek argümanlarını kullanın:

```powershell
scrapy crawl ptt_posta_kodu -a max_il=2 -a max_ilce=2 -o deneme.jsonl
```

- `max_il`: İlk N il (sıra sayfadaki `illerData` ile aynı).
- `max_ilce`: Her il için en fazla N ilçe için `postakodu` isteği gönderilir.

### PowerShell ve `-s` ayarları

`=` işaretinin yanlış ayrışmaması için tırnak kullanın:

```powershell
scrapy crawl ptt_posta_kodu -s "DOWNLOAD_DELAY=1.5" -o posta_kodlari.jsonl
```

## Çıktı alanları

| Alan        | Açıklama              |
|------------|------------------------|
| `il`       | İl adı                 |
| `ilce`     | İlçe adı               |
| `mahalle`  | Mahalle                |
| `sokak`    | Sokak / kapı aralığı   |
| `posta_kodu` | Posta kodu           |

Aynı posta kodu birden çok satırda (farklı sokaklar) tekrarlanabilir. Tamamen aynı satır (il, ilçe, mahalle, sokak, kod) tekrarlanırsa `DedupePipeline` ile elenir.

## Resmi API keşfi (özet)

Sayfa Next.js ile sunuluyor; iller listesi ilk HTML içinde `__NEXT_DATA__` → `props.pageProps.illerData` altında gelir.

İlçe ve posta kodu verisi aynı origin üzerinde şu uç ile alınır:

- **URL:** `https://www.ptt.gov.tr/api/posta-kodu`
- **Method:** `POST`
- **Headers:** `Content-Type: application/json`, `Referer` ve `Origin` olarak `https://www.ptt.gov.tr/posta-kodu` / `https://www.ptt.gov.tr` (aksi halde servis hata dönebiliyor)
- **Gövde örnekleri:**
  - `{"action":"ilceler","il_kodu":"34"}` → ilçe listesi (`kod`, `ad`)
  - `{"action":"postakodu","il_kodu":"34","ilce_kodu":"1421"}` → satır listesi (`mahalleAdi`, `sokakAdi`, `posta_Kodu`)

## 403 / “Servis hatası”

- Tarayıcı benzeri `USER_AGENT` ve yukarıdaki `Referer` / `Origin` başlıkları kullanılır (`settings.py` ve spider içinde).
- Yoğun istekte WAF devreye girebilir; `DOWNLOAD_DELAY` ve `CONCURRENT_REQUESTS_PER_DOMAIN` değerlerini artırın.
- `ROBOTSTXT_OBEY = True` varsayılandır; `robots.txt` kurallarına uyun.

## Proje yapısı

- [`postalcode_crawler/spiders/ptt_posta_kodu.py`](postalcode_crawler/spiders/ptt_posta_kodu.py) — ana örümcek
- [`postalcode_crawler/items.py`](postalcode_crawler/items.py) — alan tanımları
- [`postalcode_crawler/pipelines.py`](postalcode_crawler/pipelines.py) — tekrar ve boşluk normalizasyonu
- [`postalcode_crawler/settings.py`](postalcode_crawler/settings.py) — gecikme, başlıklar, pipeline
