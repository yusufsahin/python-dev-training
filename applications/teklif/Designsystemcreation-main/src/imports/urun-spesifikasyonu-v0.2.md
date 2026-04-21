# Teklif + Ön Muhasebe Platformu — Ürün Spesifikasyonu

**Versiyon:** v0.2 — Revize edilmiş  
**Tarih:** Nisan 2025

---

## Revizyon Notları (v0.1 → v0.2)

| Değişiklik | Açıklama |
|---|---|
| Taşındı | Epic 4 (Sipariş) Faz 2'ye alındı; teklif akışı Yol A / Yol B olarak netleştirildi |
| Taşındı | Teklif onay portalı MVP+'a çekildi |
| Revize | Epic 10 e-Belge: entegratör seçimi tasarım notu eklendi |
| Revize | Epic 13 Yetki: row-level permission tasarım notu eklendi |
| Revize | Audit log ve denetim izi Epic 13'te birleştirildi |
| Taşındı | Fiş OCR Epic 7'den çıkarıldı, Faz 2'ye eklendi |
| Revize | Nakit akış projeksiyonu Epic 8'den çıkarıldı, yalnızca Epic 11'de |
| Revize | Faz 3 → "Ürün Vizyonu" olarak yeniden adlandırıldı |

---

## 1. Ürün Amacı

Tekliften tahsilata tek akış sağlayan, KOBİ ve küçük/orta ölçekli firmalar için tasarlanmış, bulut tabanlı bir teklif + ön muhasebe platformu.

**Ana hedefler:**

- Satış ekibi hızlı teklif versin
- Teklif siparişe ve faturaya kolay dönüşsün
- Cari, stok, ödeme ve gider tek yerde toplansın
- Muhasebeci beklemeden işletme sahibi günlük operasyonu yönetsin

> **Tek cümlelik ürün tanımı:** "Tekliften tahsilata kadar satış ve ön muhasebe süreçlerini tek ekranda yöneten, bulut tabanlı ticari operasyon platformu."

---

## 2. Hedef Kullanıcılar

| Kullanıcı | Birincil İhtiyaçlar |
|---|---|
| İşletme sahibi | Nakit akışı, alacak/borç, teklif durumu, satış performansı |
| Satış / operasyon personeli | Teklif hazırlama, sipariş oluşturma, müşteri takibi, tahsilat |
| Ön muhasebe personeli | Fatura, tahsilat/ödeme, gider, banka/kasa mutabakatı |
| Muhasebeci / mali müşavir | e-Belge akışı, rapor export, kayıt kontrolü |

---

## 3. Ana Akış — Revize

Teklif onaylandıktan sonra iki geçerli yol bulunmaktadır. Karar, işletme tipine göre kullanıcı tarafından belirlenir:

- **Yol A (Doğrudan):** Onaylanan teklif → direkt satış faturasına dönüşür. Hizmet ağırlıklı işletmeler ve tek kalemli satışlar için uygundur.
- **Yol B (Sipariş üzerinden):** Onaylanan teklif → sipariş oluşturulur → kısmi sevk/faturalama yönetilir. Bu yol Faz 2'de sipariş modülü ile etkinleşir.

> MVP'de yalnızca Yol A desteklenir. Sipariş modülü gerektiren Yol B, Faz 2 kapsamındadır.

---

## 4. Ürün Modülleri

### Epic 1 — Cari / Müşteri / Tedarikçi Yönetimi

Amaç: Her ticari ilişkinin merkezde tutulması.

- Müşteri ve tedarikçi kartları
- Vergi bilgileri, adres, iletişim
- Cari bakiye, borç/alacak hareket geçmişi
- Müşteri grupları
- Risk limiti / vade limiti
- Cari bazlı notlar ve doküman ekleri
- Müşteriye özel fiyat listesi / iskonto oranı

---

### Epic 2 — Ürün / Hizmet Kataloğu

Amaç: Teklif, fatura ve stok için ortak katalog.

- Ürün/hizmet kartı
- SKU / barkod
- Birim, KDV oranı
- Satış ve alış fiyatı
- Dövizli fiyat, varyantlar
- Kategori bazlı sınıflama
- Birden fazla fiyat listesi
- Aktif/pasif ürün yönetimi

---

### Epic 3 — Teklif Yönetimi *(Revize)*

Amaç: Satışın başlangıç noktası.

- Teklif oluşturma ve şablonlar
- Teklif numaralandırma
- Müşteri bazlı özel koşullar, vade tarihi / geçerlilik süresi
- Kalem bazlı iskonto, vergi, açıklama
- PDF teklif çıktısı, e-posta / WhatsApp paylaşımı
- Teklif durum takibi: taslak / gönderildi / onaylandı / reddedildi / süresi doldu
- Teklif revizyon geçmişi ve kopyalama
- Onaylanan tekliften faturaya dönüşüm **(Yol A)**

> **Revizyon notu:** Sipariş oluşturma (Yol B) bu epic'ten çıkarıldı; Faz 2 Epic 4'e taşındı.  
> **Revizyon notu:** Teklif onay portalı MVP+'a alındı (bkz. Bölüm 5).

---

### Epic 4 — Sipariş Yönetimi *(Faz 2)*

Amaç: Teklif sonrası operasyonun kontrolü (Yol B akışı).

- Tekliften sipariş oluşturma
- Manuel sipariş girişi
- Kısmi sevk / kısmi faturalama
- Sipariş durum takibi
- Teslim tarihi ve sipariş notları
- Siparişten otomatik fatura
- Sipariş iptal / iade süreçleri

> Bu modül Faz 2'de devreye alınır.

---

### Epic 5 — Fatura ve Satış Belgeleri

Amaç: Gelir doğuran işlemleri kayıt altına almak.

- Satış faturası ve alış faturası
- Proforma, irsaliye bağlantısı
- İade faturası
- Tekrar eden faturalar
- Dövizli belge
- Belge kopyalama
- PDF / çıktı tasarımları

---

### Epic 6 — Tahsilat ve Ödeme Yönetimi

Amaç: Nakit akışını kontrol etmek.

- Tahsilat ve ödeme kaydı
- Kısmi tahsilat, fazla/eksik ödeme işleme
- Vade takip ekranı
- Geciken alacaklar
- Ödeme planı
- Tahsilat hatırlatmaları
- Müşteri ve tedarikçi ekstresi

---

### Epic 7 — Gider Yönetimi *(Revize)*

Amaç: İşletme giderlerini hızlı kaydetmek.

- Gider kategorileri
- Fiş/fatura yükleme (manuel)
- Personel masraf kaydı
- Düzenli gider tanımı
- Vergi dahil/hariç hesaplama
- Proje veya departman bazlı gider etiketleme

> **Revizyon notu:** Fiş/gider OCR bu epic'ten çıkarıldı. MVP'de manuel gider girişi yeterlidir. OCR Faz 2'ye taşındı.

---

### Epic 8 — Kasa / Banka / Çek-Senet *(Revize)*

Amaç: Parasal hareketlerin tek merkezden izlenmesi.

- Kasa hesapları
- Banka hesapları
- Para transferleri
- Banka hareket içe aktarma
- Otomatik banka entegrasyonu
- Çek/senet giriş-çıkış
- Mutabakat ekranı
- Para birimi bazlı bakiye takibi

> **Revizyon notu:** Nakit akış projeksiyonu bu epic'ten çıkarıldı. Yalnızca Epic 11 (Raporlama) kapsamındadır.

---

### Epic 9 — Stok ve Depo Yönetimi

Amaç: Satılabilir ürünlerde operasyonel doğruluk sağlamak.

- Stok giriş/çıkış
- Mevcut stok, kritik stok seviyesi uyarısı
- Tek depo (MVP+), çoklu depo (Faz 2)
- Depolar arası transfer
- Sayım/fark işlemleri
- Seri/lot takibi
- Siparişe bağlı rezervasyon
- Stok değerleme ve hareket geçmişi

---

### Epic 10 — e-Belge Yönetimi *(Revize)*

Amaç: Türkiye mevzuatına uyumlu dijital belge süreci.

- e-Fatura, e-Arşiv, e-SMM, e-İrsaliye
- Gelen/giden belge takibi
- Kabul / ret süreçleri
- Entegratör yapılandırması
- Kontör / kullanım izleme
- Belge arşivleme
- GİB uyum logları

> **Tasarım notu:** Entegratör seçimi (kendi entegratörü vs. üçüncü taraf entegratör API) bir iş kararıdır ve bu epic kapsamı dışındadır. Entegratör mimarisi ayrı bir ADR (Architecture Decision Record) ile ele alınmalıdır.

---

### Epic 11 — Raporlama ve Dashboard *(Revize)*

Amaç: İşletme sahibine anlık görünürlük vermek.

- Ana dashboard
- Bugün kesilen ve onay bekleyen teklifler
- Tahsil edilecek alacaklar, yaklaşan ödemeler
- Satış raporları, ürün kârlılığı, müşteri bazlı satış
- Gider dağılımı
- Nakit akış özeti ve projeksiyonu
- Vergi / KDV özetleri
- Export: Excel / PDF / CSV

---

### Epic 12 — Bildirim ve Görevler

Amaç: Kullanıcıyı aksiyon almaya yönlendirmek.

- Vadesi yaklaşan teklif bildirimi
- Geciken tahsilat bildirimi
- Düşük stok bildirimi
- Onay bekleyen belge bildirimi
- Yaklaşan ödeme bildirimi
- Mobil push / e-posta / uygulama içi bildirim

---

### Epic 13 — Yetki, Kullanıcı ve Şirket Ayarları *(Revize)*

Amaç: Çok kullanıcılı işletmeler için kontrol.

- Rol bazlı yetki
- Modül ve belge bazlı erişim
- Şirket / şube yapısı
- Kullanıcı aktivite logu ve denetim izi
- Özel numaralandırma ve belge ayarları
- Para birimi ve vergi ayarları

> **Tasarım notu:** Row-level permission (örn. satış temsilcisi yalnızca kendi müşteri kayıtlarını görür) MVP'de implemente edilmese de veri modelinde öngörülmelidir. Sonradan eklemek schema değişikliği gerektirir.  
> **Revizyon notu:** Audit log ve denetim izi bu epic'te birleştirildi; önceki versiyondaki tekrar giderildi.

---

### Epic 14 — Entegrasyonlar

Amaç: Ürünü merkez sistem haline getirmek.

- Banka entegrasyonları
- Sanal POS
- e-ticaret / pazaryeri entegrasyonları
- Kargo entegrasyonu
- CRM entegrasyonu
- POS / yazar kasa entegrasyonu
- Muhasebe export/import
- Açık API, webhook desteği

---

## 5. Faz Planı

### MVP — Olmazsa olmaz

- Kullanıcı / şirket ayarları
- Cari yönetimi (Epic 1)
- Ürün / hizmet kartları (Epic 2)
- Teklif oluşturma ve PDF paylaşımı
- Teklif durum takibi
- Tekliften faturaya dönüşüm (Yol A)
- Satış / alış faturası
- Tahsilat / ödeme kayıtları
- Temel banka / kasa
- Gider yönetimi (manuel)
- Temel raporlar ve dashboard
- Rol bazlı yetki ve denetim izi

### MVP+ — İlk lansmanla birlikte

- e-Fatura / e-Arşiv (Epic 10)
- Stok — tek depo (Epic 9)
- Vade hatırlatmaları
- Mobil responsive kullanım
- **Teklif onay portalı** — müşteri linke tıklayıp onaylasın, revizyon istesin, ön ödeme yapsın

> Teklif onay portalı düşük maliyetli, yüksek değerli bir ayrıştırıcıdır. Rakip ürünlerin çoğunda bulunmamaktadır.

### Faz 2 — Ticaret genişlemesi

- Sipariş yönetimi (Epic 4 / Yol B)
- Çoklu depo
- Çek/senet
- Fiş / gider OCR
- Tekrar eden faturalar
- Banka otomatik mutabakat
- Gelişmiş dashboard
- CRM pipeline
- Sanal POS
- e-ticaret entegrasyonları
- Müşteri portalı genişletmesi
- Elektronik imza / dijital onay

---

## 6. Ürün Vizyonu

Aşağıdaki özellikler stakeholder öncelik kararları için yol haritasında görünür tutulmaktadır. Bunlar ayrı ürün katmanları veya add-on modüller olarak ele alınmalı; core backlog'a eklenmemelidir.

- Yapay zekâ ile teklif önerisi
- Müşteri bazlı fiyat optimizasyonu
- Tahsilat risk skoru
- Nakit akış tahmini (AI)
- Otomatik belge sınıflandırma
- Anomali tespiti
- Bayi / saha satış modu
- Çok şirketli yapı
- Franchise / şube merkezi yönetimi

---

## 7. Fark Yaratıcı Özellikler

Ürünün rakiplerden ayrışacağı yüksek değerli alanlar:

**Teklif sihirbazı**
- Hazır şablonlar, sektör bazlı teklif metinleri
- Otomatik ödeme planı önerisi
- Teklif karşılaştırma görünümü

**Teklif onay portalı (MVP+)**
- Müşteri linke tıklayıp onaylasın
- Revizyon istesin
- Ön ödeme yapsın

**Akıllı tahsilat (Faz 2)**
- Gecikme riski yüksek müşterileri işaretle
- Otomatik hatırlatma akışları

**İşletme sahibi modu**
- Çok sade ana dashboard
- "Bugün neye müdahale etmeliyim?" ekranı

**Muhasebeci işbirliği modu**
- Mali müşavir erişim rolü
- Export paketleri
- Dönem sonu kontrol listeleri

---

## 8. Paket Konumlandırması

| | Paket 1 — Teklif | Paket 2 — Teklif + Ön Muhasebe | Paket 3 — Ticaret |
|---|:---:|:---:|:---:|
| Cari yönetimi | ✓ | ✓ | ✓ |
| Ürün/hizmet kataloğu | ✓ | ✓ | ✓ |
| Teklif oluşturma | ✓ | ✓ | ✓ |
| PDF paylaşımı | ✓ | ✓ | ✓ |
| Teklif dashboard | ✓ | ✓ | ✓ |
| Fatura (Yol A) | — | ✓ | ✓ |
| Tahsilat / ödeme | — | ✓ | ✓ |
| Gider yönetimi | — | ✓ | ✓ |
| Banka / kasa | — | ✓ | ✓ |
| Temel raporlar | — | ✓ | ✓ |
| Stok / depo | — | — | ✓ |
| Sipariş yönetimi (Yol B) | — | — | ✓ |
| e-Fatura / e-Arşiv | — | — | ✓ |
| Entegrasyonlar | — | — | ✓ |
| Gelişmiş raporlar | — | — | ✓ |
