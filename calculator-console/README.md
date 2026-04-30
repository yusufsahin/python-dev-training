# Python Flask Hesap Makinesi

Bu proje, başlangıçta console tabanlı olan bir hesap makinesinin Flask ile modern bir web uygulamasına dönüştürülmüş halidir.

## Özellikler

- **Web Arayüzü**: Modern, premium tasarımlı ve responsive web arayüzü.
- **Dört İşlem**: Toplama, çıkarma, çarpma ve bölme.
- **Hata Yönetimi**: Sıfıra bölme ve geçersiz giriş kontrolleri.
- **CLI Desteği**: Geriye dönük uyumluluk için console arayüzü korunmuştur.
- **Test Piramidi**: Unit, integration, web ve system testlerini içeren kapsamlı test altyapısı.

## Dosya Yapısı

```text
calculator-console/
├── calculator/         # Domain mantığı (hesaplama, validasyon, formatlama)
│   ├── __init__.py
│   ├── operations.py
│   ├── formatting.py
│   └── validation.py
├── static/             # Statik dosyalar (CSS)
│   └── css/styles.css
├── templates/          # HTML şablonları
│   └── index.html
├── tests/              # Test katmanları
│   ├── unit/           # Birim testleri
│   ├── integration/    # Modül entegrasyon testleri
│   ├── web/            # Flask web route testleri
│   ├── ui/             # Playwright tarayıcı UI testleri
│   ├── system/         # Subprocess ile uçtan uca testler
│   └── uat/            # Kullanıcı kabul testleri
├── app.py              # Flask uygulama ana dosyası
├── main.py             # Console arayüzü ana dosyası
├── requirements.txt    # Uygulama bağımlılıkları
├── requirements-dev.txt # Geliştirme bağımlılıkları
├── pytest.ini          # Pytest yapılandırması
└── README.md
```

## Kurulum

1. Sanal ortam oluşturun ve aktifleştirin:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Windows için: .venv\Scripts\activate
   ```

2. Bağımlılıkları yükleyin:
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt
   ```

## Çalıştırma

### Web Uygulaması
```bash
flask --app app run
# veya
python app.py
```

### Console Uygulaması
```bash
python main.py
```

## Testler

Tüm testleri çalıştırmak için:
```bash
$env:PYTHONPATH = "."; pytest  # PowerShell
# veya
PYTHONPATH=. pytest           # Bash
```

Belirli katmanları çalıştırmak için:
- **Unit**: `pytest -m unit`
- **Web**: `pytest -m web`
- **UI (Playwright)**: `pytest tests/ui -m ui` (ilk kurulumda tarayıcı: `playwright install chromium`)
- **Integration**: `pytest -m integration`

### Playwright UI testleri (tarayıcıda görmek için)

İlk kurulumda Chromium indirin:

```bash
playwright install chromium
```

Headed mod (pencere açık):

```powershell
pytest tests/ui -m ui --headed
```

`tests/ui` testleri varsayılan olarak **her işlem arasında ~1 saniye** yavaşlatılır (`slow_mo`); komut satırıyla üzerine yazılır:

```powershell
pytest tests/ui -m ui --headed --slowmo 2000
pytest tests/ui -m ui --headed --slowmo 0
```

Ortam değişkeni (CLI ile birlikte kullanılabilir):

```powershell
$env:PLAYWRIGHT_UI_SLOWMO = "500"; pytest tests/ui -m ui --headed
```

Kapsam (coverage) raporu — uygulama kodu (`calculator/`, `main.py`, `app.py`; `tests/` hariç):
```bash
pytest --cov --cov-config=.coveragerc --cov-report=term-missing
```

## Gereksinimler

- Python 3.8+
- Flask 3.0+
