# Flask Web App Migration Plan

## Amaç

Mevcut console tabanlı hesap makinesi uygulamasını Flask ile çalışan basit bir web uygulamasına dönüştürmek. Bu plan yalnızca migration yol haritasıdır; mevcut Python kodunda uygulama değişikliği yapılmamıştır.

## Mevcut Durum Özeti

- Uygulama tek dosyada çalışıyor: `main.py`.
- Matematik işlemleri saf fonksiyonlar halinde mevcut: `add`, `subtract`, `multiply`, `divide`.
- CLI etkileşimi aynı dosyada: `show_menu`, `get_operation_choice`, `get_number`, `main`.
- Sonuç gösterimi `format_for_display` ile yapılıyor.
- Test yapısı güçlü: unit, integration, system ve UAT katmanları var.
- Mevcut sistem testleri `python main.py` ve stdin/stdout akışına bağlı.
- Projede henüz Flask, template, static dosya veya web test altyapısı bulunmuyor.

## Hedef Mimari

```text
calculator-console/
|
|-- app.py
|-- calculator/
|   |-- __init__.py
|   |-- operations.py
|   |-- formatting.py
|   `-- validation.py
|-- templates/
|   `-- index.html
|-- static/
|   |-- css/
|   |   `-- styles.css
|   `-- js/
|       `-- app.js              # opsiyonel, ilk fazda zorunlu değil
|-- tests/
|   |-- unit/
|   |-- integration/
|   |-- web/
|   `-- system/
|-- requirements.txt
|-- requirements-dev.txt
|-- README.md
`-- MIGRATION_PLAN.md
```

## Migration Stratejisi

### Faz 1 - Domain Kodunu CLI'dan Ayırma

Amaç, hesaplama mantığını Flask'a bağımlı olmadan tekrar kullanılabilir hale getirmek.

Yapılacaklar:

1. `calculator/` dizinini oluştur.
2. `calculator/__init__.py` oluştur. Bu dosya boş bırakılabilir ya da `operations.py` ve `formatting.py`'deki temel fonksiyonları yeniden dışa aktaracak şekilde düzenlenebilir. Dosyanın varlığı `calculator/`'ı geçerli bir Python paketi yapar ve ilerleyen fazlarda `from calculator import add` gibi kısa import yollarına olanak tanır.
3. `calculator/operations.py` oluştur.
4. `add`, `subtract`, `multiply`, `divide` fonksiyonlarını buraya taşı.
5. `calculator/formatting.py` oluştur.
6. `format_for_display` fonksiyonunu buraya taşı.
7. `main.py` dosyasını geçici olarak koru ve yeni modüllerden import edecek şekilde sadeleştir. CLI'ya ait `show_menu`, `get_operation_choice`, `get_number`, `main` fonksiyonları ve `if __name__ == "__main__":` bloğu bu aşamada `main.py`'de kalmaya devam eder. Modül düzeyindeki UTF-8 stdout yapılandırma kodu da bu aşamada `main.py`'de korunur.
8. Mevcut unit test importlarını yeni modül yollarına güncelle:
   - `tests/unit/test_operations.py`: `from main import add, subtract, multiply, divide` → `from calculator.operations import add, subtract, multiply, divide`
   - `tests/unit/test_format_display.py`: `from main import format_for_display` → `from calculator.formatting import format_for_display`
   - `tests/unit/test_startup.py`: Bu test `main.py`'deki `sys.stdout.reconfigure` bloğunu `importlib` ile doğrudan test eder. UTF-8 yapılandırma kodu bu fazda `main.py`'de kaldığı için herhangi bir değişiklik gerektirmez.
9. `tests/integration/` testlerinin durumunu doğrula: `test_cli_flow.py` ve `test_entrypoint.py`, `main.py`'yi import etmeye devam eder. `main.py` sadeleştirilip yeni modülleri import edecek şekilde güncellendiğinden bu testler değişiklik gerektirmeden çalışmayı sürdürür.

Kabul kriterleri:

- `pytest -m unit` başarılı çalışmalı.
- `pytest -m integration` başarılı çalışmalı.
- CLI davranışı (`python main.py`) bozulmamalı.
- Flask bağımlılığı bu fazda eklenmek zorunda değil.

### Faz 2 - Web Girdi Modeli ve Validasyon

Amaç, web formundan gelen string verileri kontrollü şekilde doğrulamak.

Not: Bu fazdaki validasyon fonksiyonları saf Python'dur ve Flask'a bağımlı değildir. Testler standart `pytest` komutu ile çalıştırılır; Flask test client'ı bu fazda gerekmez.

Yapılacaklar:

1. `calculator/validation.py` oluştur.
2. Desteklenen operasyonları tanımla: `add`, `subtract`, `multiply`, `divide`.
3. Form alanları için doğrulama fonksiyonu ekle:
   - `operation`
   - `first_number`
   - `second_number`
4. Boş değer, geçersiz sayı ve sıfıra bölme durumları için kullanıcıya gösterilecek hata mesajlarını standartlaştır.
5. Validasyon fonksiyonlarını unit testlerle kapsa. Bu testler `tests/unit/test_validation.py` olarak eklenebilir; Flask gerektirmez.

Kabul kriterleri:

- Geçerli sayı ve geçerli operasyon girildiğinde validasyon hata üretmemeli ve işlem yapılabilir olmalı (mutlu yol).
- Geçersiz sayı girildiğinde işlem yapılmamalı.
- Boş form alanları kullanıcı dostu hata üretmeli.
- Sıfıra bölme web tarafında da engellenmeli.

### Faz 3 - Flask Uygulama İskeleti

Amaç, minimal Flask uygulamasını ayağa kaldırmak.

Yapılacaklar:

1. `requirements.txt` oluştur ve Flask bağımlılığını açık sürüm sabitleme ile ekle:

   ```text
   Flask>=3.0.0
   ```

   Daha geniş Python 3.8/3.9 uyumluluğu gerekiyorsa `Flask>=2.3.0` tercih edilebilir; bu durumun açıkça belgelenmesi önerilir.
2. `app.py` oluştur.
3. Flask application factory tercih edilecekse `create_app()` kullan; proje küçük tutulacaksa doğrudan `app = Flask(__name__)` yeterli.
4. `/` route'u ekle:
   - `GET`: hesap makinesi formunu gösterir.
   - `POST`: form verisini doğrular, işlemi yapar, sonucu veya hatayı gösterir.
   - Önemli: `divide()` fonksiyonu sıfıra bölme durumunda `None` döndürür. Route içinde `result = divide(a, b)` çağrısından sonra mutlaka `if result is None:` kontrolü yapılmalı ve bu durumda template'e kullanıcı dostu bir hata mesajı iletilmeli. `None` değeri doğrudan template'e geçirilmemeli.
5. `templates/index.html` oluştur.
6. Basit ama kullanılabilir form arayüzü kur:
   - iki sayı input'u
   - işlem seçimi
   - hesapla butonu
   - sonuç alanı
   - hata alanı

Kabul kriterleri:

- `flask --app app run` veya `python app.py` ile uygulama çalışmalı.
- Ana sayfa 200 HTTP status dönmeli.
- Form gönderildiğinde sonuç aynı sayfada görünmeli.
- Sıfıra bölme durumunda uygulama çökmemeli, hata mesajı göstermeli.

### Faz 4 - UI ve Kullanıcı Deneyimi

Amaç, console menüsünü web'e doğal bir form deneyimi olarak taşımak.

Yapılacaklar:

1. `static/css/styles.css` oluştur.
2. Formu masaüstü ve mobil ekranlarda okunabilir hale getir.
3. İşlem seçimi için select veya radio button kullan.
4. Hata mesajlarını form alanlarına yakın göster.
5. Son işlemi kullanıcıya açık formatta göster:

```text
Sonuç: 10 + 5 = 15
```

Kabul kriterleri:

- UI mobil genişlikte taşmamalı.
- Hatalar ve sonuç aynı anda karışık görünmemeli.
- Türkçe metinler düzgün encoding ile görünmeli.

### Faz 5 - Testlerin Web'e Uyarlanması

Amaç, mevcut test piramidini web uygulamasına göre güncellemek.

Yapılacaklar:

1. Unit testleri domain modüllerinde koru.

2. `pytest.ini` dosyasını güncelle ve `markers` bölümüne `web` marker'ını ekle:

   ```ini
   web: Flask test client ile HTTP katmanı testleri
   ```

   Bu adım atlanırsa `pytest -m web` komutu bilinmeyen marker uyarısı üretir.

3. `tests/web/` dizinini oluştur.

4. `tests/web/conftest.py` oluştur ve Flask test client fixture'ını buraya ekle:

   ```python
   import pytest
   from app import app as flask_app

   @pytest.fixture
   def client():
       flask_app.config["TESTING"] = True
       with flask_app.test_client() as c:
           yield c
   ```

   Bu fixture olmadan her test dosyası uygulama kurulumunu tekrar eder ve bakımı zorlaşır.

5. `tests/web/` altında web testi dosyalarını oluştur. Test edilecek web senaryoları:
   - `GET /` başarılı döner.
   - Toplama sonucu doğru gösterilir.
   - Çıkarma sonucu doğru gösterilir.
   - Çarpma sonucu doğru gösterilir.
   - Bölme sonucu doğru gösterilir.
   - Sıfıra bölme hata mesajı gösterilir.
   - Boş sayı alanı hata mesajı gösterilir.
   - Sayı yerine metin girilirse hata mesajı gösterilir.

6. `tests/web/__init__.py` dosyası hakkında karar ver: Mevcut `tests/unit/`, `tests/integration/`, `tests/system/` ve `tests/uat/` dizinlerinde `__init__.py` dosyası bulunmamaktadır. Tutarlılık için `tests/web/` dizinine de `__init__.py` eklenmemesi önerilir. Eklenecekse tüm test dizinlerine aynı anda eklenmeli.

7. CLI test dosyalarının durumunu netleştir:
   - `tests/integration/test_cli_flow.py` ve `tests/integration/test_entrypoint.py`: CLI (`main.py`'deki `main()` ve `if __name__ == "__main__":`) korunuyorsa bu testler geçerliliğini sürdürür. CLI tamamen kaldırılacaksa her iki dosya arşivlenmeli ya da silinmeli ve yerlerini işlevsel olarak karşılayan web testleri yazılmalıdır.
   - `tests/system/test_subprocess_e2e.py` ve `tests/uat/test_acceptance_scenarios.py`: Bu testler `python main.py`'yi subprocess ile çalıştırır. CLI kaldırıldığında geçersiz hale gelir. Karar Faz 5 sonunda alınmalı ve belgelenmeli.

Kabul kriterleri:

- `pytest` tüm aktif testleri çalıştırmalı.
- `pytest -m web` yalnızca web testlerini çalıştırmalı ve uyarı vermemeli.
- Web route testleri Flask test client ile dış sunucu başlatmadan çalışmalı.
- Coverage komutu yeni modül yollarını kapsamalı: `pytest --cov=calculator --cov=app --cov-report=term-missing`.

### Faz 6 - README ve Çalıştırma Talimatları

Amaç, projenin web uygulaması olarak nasıl çalıştırılacağını netleştirmek.

Yapılacaklar:

1. README başlığını web uygulamasını yansıtacak şekilde güncelle.
2. Kurulum komutlarını ekle:

   ```bash
   python -m venv .venv
   pip install -r requirements.txt
   pip install -r requirements-dev.txt
   ```

3. Çalıştırma komutunu ekle:

   ```bash
   flask --app app run
   ```

4. Test komutlarını güncelle:

   ```bash
   pytest
   pytest -m unit
   pytest -m web
   ```

5. CLI korunuyorsa ayrıca `python main.py` komutu bırakılır.

Kabul kriterleri:

- Yeni geliştirici README üzerinden uygulamayı çalıştırabilmeli.
- Console/web ayrımı açıkça belirtilmeli.

## Önerilen İlk Teknik Karar

İlk migration adımında CLI tamamen silinmemeli. Önce hesaplama mantığı modüllere ayrılmalı, sonra Flask arayüzü aynı domain fonksiyonlarını kullanmalı. Bu yaklaşım mevcut testlerin büyük kısmını korur ve dönüşüm riskini azaltır.

## Riskler ve Dikkat Noktaları

- `main.py` içinde Türkçe metinlerde encoding sorunu görünüyor. Web dönüşümünde tüm dosyalar UTF-8 olarak kaydedilmeli.
- `main.py`'deki modül düzeyindeki UTF-8 stdout yapılandırma kodu CLI'ya özgüdür. `app.py`'de bu koda gerek yoktur; Flask WSGI ortamında stdout yönlendirme farklı çalışır. `test_startup.py` testi `main.py`'yi doğrudan test ettiğinden CLI var olduğu sürece geçerliliğini korur; CLI kaldırıldığında bu test de kaldırılmalıdır.
- Mevcut integration/system testleri CLI'ya bağlı; Flask dönüşümünde bu testlerin bir kısmı geçersiz hale gelecek. Faz 5'te açık karar verilmesi gerekir.
- `divide` fonksiyonu sıfıra bölmede `None` döndürür; exception fırlatmaz. Web route'unda `result = divide(a, b)` çağrısının hemen ardından `if result is None:` kontrolü yapılmalı, bu durumda kullanıcı dostu hata mesajı template'e iletilmeli, `None` değeri template'e ham olarak geçirilmemeli.
- Float formatlama web ve CLI arasında aynı kalmalı; sonuç gösterimi tek fonksiyondan yapılmalı.
- Flask formundan gelen tüm değerler string olacağı için sayı dönüşümü route içinde dağınık yapılmamalı, validasyon modülünde toplanmalı.
- `Flask>=3.0.0` gerektirmek Python 3.8 desteğini düşürür. Hedef Python sürümü `requirements.txt`'te ya da README'de açıkça belirtilmeli.

## Önerilen Sıralı İş Listesi

1. `calculator/` paketini oluştur (`__init__.py` dahil).
2. Hesaplama ve formatlama fonksiyonlarını taşı.
3. Unit test importlarını güncelle; `test_startup.py`'nin değişmediğini doğrula.
4. CLI'nın yeni modüllerle hâlâ çalıştığını doğrula (`pytest -m integration` ve `python main.py`).
5. `calculator/validation.py`'yi oluştur ve saf pytest ile test et.
6. Flask bağımlılığını ekle (`requirements.txt`, `Flask>=3.0.0`).
7. `app.py`, `templates/index.html`, `static/css/styles.css` dosyalarını oluştur.
8. Route içinde `divide()` `None` dönüş kontrolünü uygula.
9. `pytest.ini`'e `web` marker'ını ekle.
10. `tests/web/conftest.py`'yi `client` fixture'ı ile oluştur.
11. Flask test client testlerini yaz.
12. CLI testlerinin korunup korunmayacağına karar ver; kararı belgele.
13. README'yi web uygulamasına göre güncelle.

## Nihai Kabul Kriterleri

- Kullanıcı tarayıcıdan iki sayı girip dört işlem yapabilmeli.
- Sıfıra bölme kullanıcı dostu hata mesajı göstermeli.
- Boş veya geçersiz sayı girişi uygulamayı çökertmemeli.
- Sonuçlar mevcut console formatıyla uyumlu gösterilmeli.
- Domain fonksiyonları Flask'tan bağımsız test edilebilmeli.
- Web route'ları otomatik testlerle kapsanmalı.
- Proje README üzerinden kurulup çalıştırılabilmeli.
