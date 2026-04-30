# Python Console 4 İşlem Hesap Makinesi — Cursor Ready Gereksinim Dokümanı

## 1. Amaç

Bu projenin amacı, Python ile çalışan basit, anlaşılır ve kullanıcı dostu bir console uygulaması geliştirmektir.

Uygulama kullanıcıdan iki sayı ve yapmak istediği matematiksel işlemi alacak, sonucu ekrana yazdıracaktır.

Desteklenecek işlemler:

- Toplama
- Çıkarma
- Çarpma
- Bölme

Uygulama başlangıç seviyesi Python öğrenen biri için anlaşılır, sade ve fonksiyonlara ayrılmış şekilde geliştirilecektir.

---

## 2. Teknoloji Gereksinimleri

- Programlama dili: Python 3.x
- Arayüz: Console / Terminal
- Harici kütüphane kullanılmayacak.
- Kod `main.py` dosyasında yer alacak.
- Proje içinde ayrıca `README.md` dosyası bulunacak.

---

## 3. Beklenen Dosya Yapısı

```text
calculator-console/
│
├── main.py
└── README.md
```

> Not: `calculator-console/` klasörü, eğitim deposunun kök dizininde oluşturulur. Projeyi farklı bir konumda geliştiriyorsan klasörü istediğin yola taşıyabilirsin; içerik ve çalıştırma komutu değişmez.

---

## 4. Uygulama Açılışı

Program başladığında kullanıcıya kısa bir karşılama mesajı gösterilecektir.

Örnek:

```text
Python Console Hesap Makinesi
-----------------------------
```

---

## 5. Menü Gereksinimi

Kullanıcıya aşağıdaki işlem menüsü gösterilecektir:

```text
Lütfen yapmak istediğiniz işlemi seçiniz:

1 - Toplama
2 - Çıkarma
3 - Çarpma
4 - Bölme
5 - Çıkış
```

Kullanıcıdan seçim alınacaktır.

Geçerli seçimler:

```text
1, 2, 3, 4, 5
```

---

## 6. Menü Seçimi Kuralları

Kullanıcı geçerli bir seçim yaparsa ilgili işlem çalıştırılacaktır.

Kullanıcı geçersiz bir seçim yaparsa hata mesajı gösterilecek ve menü tekrar gösterilecektir.

Örnek hata mesajı:

```text
Geçersiz seçim yaptınız. Lütfen 1 ile 5 arasında bir değer giriniz.
```

Geçersiz seçim örnekleri:

```text
0
6
abc
+
boş giriş
```

---

## 7. Kullanıcıdan Sayı Alma Gereksinimi

Kullanıcı işlem seçtikten sonra iki sayı girecektir.

Örnek:

```text
Birinci sayıyı giriniz:
İkinci sayıyı giriniz:
```

Desteklenecek sayı tipleri:

```text
10
-10
10.5
-3.25
0
```

Kullanıcı sayı yerine metin girerse hata mesajı gösterilecek ve tekrar sayı istenecektir.

Örnek hata mesajı:

```text
Hatalı giriş. Lütfen geçerli bir sayı giriniz.
```

---

## 8. Toplama İşlemi

Kullanıcı menüden `1` seçerse iki sayı toplanacaktır.

Örnek:

```text
Birinci sayıyı giriniz: 10
İkinci sayıyı giriniz: 5

Sonuç: 10 + 5 = 15
```

---

## 9. Çıkarma İşlemi

Kullanıcı menüden `2` seçerse birinci sayıdan ikinci sayı çıkarılacaktır.

Örnek:

```text
Birinci sayıyı giriniz: 10
İkinci sayıyı giriniz: 5

Sonuç: 10 - 5 = 5
```

---

## 10. Çarpma İşlemi

Kullanıcı menüden `3` seçerse iki sayı çarpılacaktır.

Örnek:

```text
Birinci sayıyı giriniz: 10
İkinci sayıyı giriniz: 5

Sonuç: 10 * 5 = 50
```

---

## 11. Bölme İşlemi

Kullanıcı menüden `4` seçerse birinci sayı ikinci sayıya bölünecektir.

Örnek:

```text
Birinci sayıyı giriniz: 10
İkinci sayıyı giriniz: 5

Sonuç: 10 / 5 = 2
```

Eğer ikinci sayı `0` ise işlem yapılmayacak ve kullanıcıya hata mesajı gösterilecektir.

Örnek:

```text
Sıfıra bölme hatası. İkinci sayı 0 olamaz.
```

---

## 12. Çıkış İşlemi

Kullanıcı menüden `5` seçerse program kapanacaktır.

Örnek:

```text
Programdan çıkılıyor. Görüşmek üzere.
```

---

## 13. Döngü Davranışı

Program tek işlemden sonra kapanmamalıdır.

Her işlemden sonra kullanıcıya tekrar menü gösterilmelidir.

Kullanıcı `5 - Çıkış` seçeneğini seçene kadar uygulama çalışmaya devam etmelidir.

---

## 14. Fonksiyonel Gereksinimler

Aşağıdaki fonksiyonlar yazılmalıdır.

---

### 14.1. `show_menu()`

Menüyü console ekranına yazdırır.

Sorumlulukları:

- Menü başlığını gösterir.
- Toplama, çıkarma, çarpma, bölme ve çıkış seçeneklerini gösterir.
- Kullanıcıdan veri almaz.
- Sadece ekrana yazdırma işlemi yapar.
- `main()` döngüsünde her tur başında `get_operation_choice()` çağrısından önce çağrılır.

---

### 14.2. `get_operation_choice()`

Kullanıcıdan işlem seçimini alır.

Sorumlulukları:

- Kullanıcıdan seçim ister.
- Kullanıcı girişine baştaki ve sondaki boşlukları temizlemek için `.strip()` uygulanır.
- Seçimin `1`, `2`, `3`, `4` veya `5` olup olmadığını kontrol eder.
- Geçersiz seçimlerde hata mesajı gösterir.
- Geçerli seçim yapılana kadar tekrar seçim ister.
- Geçerli seçimi geri döndürür.

---

### 14.3. `get_number(message)`

Kullanıcıdan sayı alır.

Parametre:

```python
message
```

Sorumlulukları:

- Parametre olarak gelen mesajı kullanıcıya gösterir.
- Kullanıcıdan giriş alır.
- Girişin sayıya çevrilip çevrilemediğini kontrol eder.
- Geçersiz girişte hata mesajı gösterir.
- Geçerli sayı girilene kadar tekrar ister.
- Sayıyı `float` olarak geri döndürür.
- Sonuç tam sayıya eşitse (ör. `15.0`) ekranda `15` olarak gösterilmesi için `main()` içinde formatlama yapılır; bu fonksiyon yalnızca ham `float` döndürür.

---

### 14.4. `add(a, b)`

İki sayıyı toplar.

Parametreler:

```python
a
b
```

Geri dönüş:

```python
a + b
```

---

### 14.5. `subtract(a, b)`

Birinci sayıdan ikinci sayıyı çıkarır.

Parametreler:

```python
a
b
```

Geri dönüş:

```python
a - b
```

---

### 14.6. `multiply(a, b)`

İki sayıyı çarpar.

Parametreler:

```python
a
b
```

Geri dönüş:

```python
a * b
```

---

### 14.7. `divide(a, b)`

Birinci sayıyı ikinci sayıya böler.

Parametreler:

```python
a
b
```

Kurallar:

- Eğer `b == 0` ise fonksiyon `None` döndürür; hata mesajını `main()` yazar. Fonksiyon kendi içinde print yapmaz.
- Geçerli durumda `a / b` sonucu `float` olarak döndürülür.

---

### 14.8. `main()`

Uygulamanın ana akışını yönetir.

Sorumlulukları:

- Açılış mesajını gösterir.
- Menü döngüsünü başlatır.
- Kullanıcıdan işlem seçimini alır.
- Gerekirse kullanıcıdan iki sayı alır.
- Seçilen işleme göre ilgili fonksiyonu çağırır.
- Sonucu ekrana yazdırır.
- Kullanıcı çıkış seçeneğini seçene kadar uygulamayı çalıştırır.

---

## 15. Hata Yönetimi

Aşağıdaki hata durumları yönetilmelidir:

| Durum | Beklenen Davranış |
|---|---|
| Kullanıcı menüde geçersiz seçim yaparsa | Hata mesajı göster, tekrar seçim iste |
| Kullanıcı sayı yerine metin girerse | Hata mesajı göster, tekrar sayı iste |
| Kullanıcı boş giriş yaparsa | Hata mesajı göster, tekrar giriş iste |
| Kullanıcı bölmede ikinci sayıya `0` girerse | Sıfıra bölme hatası göster, menüye dön |
| Program beklenmeyen şekilde kapanmamalı | Giriş hataları kontrollü şekilde yönetilmeli |

---

## 16. Kodlama Standartları

Kod aşağıdaki standartlara uygun olmalıdır:

- Kod sade ve okunabilir olmalıdır.
- Fonksiyon isimleri İngilizce olmalıdır.
- Kullanıcıya gösterilen mesajlar Türkçe olmalıdır.
- Harici kütüphane kullanılmamalıdır.
- Global değişken kullanılmamalıdır. Döngü sayacı veya bayrak gibi değişkenler `main()` fonksiyonu içinde yerel olarak tanımlanmalıdır.
- Tekrarlayan kodlar fonksiyonlara ayrılmalıdır.
- `if __name__ == "__main__":` bloğu kullanılmalıdır.
- `try-except` ile sayı giriş hataları yönetilmelidir.
- Başlangıç seviyesi Python öğrenen biri kodu okuyunca anlayabilmelidir.
- Gereksiz karmaşık yapı kullanılmamalıdır.

---

## 17. Örnek Kullanım Akışı

```text
Python Console Hesap Makinesi
-----------------------------

Lütfen yapmak istediğiniz işlemi seçiniz:

1 - Toplama
2 - Çıkarma
3 - Çarpma
4 - Bölme
5 - Çıkış

Seçiminiz: 1

Birinci sayıyı giriniz: 10
İkinci sayıyı giriniz: 5

Sonuç: 10 + 5 = 15

Lütfen yapmak istediğiniz işlemi seçiniz:

1 - Toplama
2 - Çıkarma
3 - Çarpma
4 - Bölme
5 - Çıkış

Seçiminiz: 4

Birinci sayıyı giriniz: 10
İkinci sayıyı giriniz: 0

Sıfıra bölme hatası. İkinci sayı 0 olamaz.

Lütfen yapmak istediğiniz işlemi seçiniz:

1 - Toplama
2 - Çıkarma
3 - Çarpma
4 - Bölme
5 - Çıkış

Seçiminiz: 5

Programdan çıkılıyor. Görüşmek üzere.
```

---

## 18. README.md Gereksinimleri

Proje içinde `README.md` dosyası oluşturulmalıdır.

README içeriğinde aşağıdaki başlıklar bulunmalıdır:

```md
# Python Console Hesap Makinesi

Bu proje Python ile geliştirilmiş basit bir console hesap makinesi uygulamasıdır.

## Özellikler

- Toplama
- Çıkarma
- Çarpma
- Bölme
- Sıfıra bölme kontrolü
- Geçersiz giriş kontrolü
- Sürekli çalışan menü sistemi

## Dosya Yapısı

```text
calculator-console/
│
├── main.py
└── README.md
```

## Çalıştırma

```bash
python main.py
```

## Gereksinimler

- Python 3.x

## Kullanım

Program çalıştırıldığında kullanıcıdan işlem seçmesi istenir.

Desteklenen işlemler:

- 1: Toplama
- 2: Çıkarma
- 3: Çarpma
- 4: Bölme
- 5: Çıkış

Kullanıcı çıkış seçeneğini seçene kadar program çalışmaya devam eder.
```

---

## 19. Kabul Kriterleri

Uygulama aşağıdaki kriterleri sağlamalıdır:

- Kullanıcı menüden işlem seçebilmelidir.
- Menüde 5 seçenek bulunmalıdır.
- Kullanıcı iki sayı girebilmelidir.
- Toplama işlemi doğru çalışmalıdır.
- Çıkarma işlemi doğru çalışmalıdır.
- Çarpma işlemi doğru çalışmalıdır.
- Bölme işlemi doğru çalışmalıdır.
- Sıfıra bölme engellenmelidir.
- Geçersiz menü seçimi kontrol edilmelidir.
- Sayı yerine metin girilirse uygulama hata vermeden tekrar giriş istemelidir.
- Boş giriş yapılırsa uygulama hata vermeden tekrar giriş istemelidir.
- Kullanıcı çıkış seçeneğini seçene kadar uygulama çalışmaya devam etmelidir.
- Kod fonksiyonlara ayrılmış olmalıdır.
- Program `main.py` üzerinden çalıştırılabilmelidir.
- Harici kütüphane kullanılmamalıdır.
- `README.md` dosyası oluşturulmalıdır.

---

## 20. Cursor İçin Uygulama Talimatı

Aşağıdaki talimatları uygula:

1. Python 3 ile console tabanlı dört işlem hesap makinesi geliştir.
2. Proje klasörü adı `calculator-console` olsun.
3. `main.py` dosyasını oluştur.
4. `README.md` dosyasını oluştur.
5. Harici kütüphane kullanma.
6. Kullanıcı mesajlarını Türkçe yaz.
7. Fonksiyon isimlerini İngilizce yaz.
8. Menü sistemi sürekli çalışsın.
9. Kullanıcı `5 - Çıkış` seçeneğini seçince program kapansın.
10. Hatalı girişleri `try-except` ile yönet.
11. Sıfıra bölme hatasını özel olarak kontrol et.
12. Kod sade, okunabilir ve başlangıç seviyesine uygun olsun.
13. Program `python main.py` komutu ile çalıştırılabilir olsun.
14. Kodda `if __name__ == "__main__":` bloğunu kullan.
15. Yorumları yalnızca anlaşılması güç bloklara ekle (ör. `try-except` bloğu, sıfıra bölme koşulu). Fonksiyon adı zaten ne yaptığını anlatıyorsa yorum yazma.

---

## 21. Cursor İçin Nihai Prompt

Bu gereksinim dokümanına göre Python 3 ile console tabanlı dört işlem hesap makinesi uygulamasını eksiksiz geliştir.

Beklenen çıktı:

- `calculator-console/main.py`
- `calculator-console/README.md`

Kurallar:

- Harici kütüphane kullanma.
- Kullanıcı mesajları Türkçe olsun.
- Fonksiyon isimleri İngilizce olsun.
- Program sürekli çalışan menü yapısına sahip olsun.
- Kullanıcı çıkış seçeneğini seçene kadar program kapanmasın.
- Geçersiz menü seçimleri kontrol edilsin.
- Geçersiz sayı girişleri kontrol edilsin.
- Sıfıra bölme hatası kontrol edilsin.
- Kod okunabilir, sade ve başlangıç seviyesi için anlaşılır olsun.
- README dosyası proje açıklamasını ve çalıştırma komutunu içersin.

Önce dosya yapısını oluştur, sonra `main.py` ve `README.md` dosyalarını eksiksiz üret.