# 11 — Kurulum ve Konfigürasyon

## Ön Gereksinimler
- Python 3.12+
- pip
- Git

---

## 1. Proje Kurulumu

```bash
# Çalışma dizinine git
cd storium-modulith

# Virtual environment oluştur
python -m venv .venv

# Aktif et
source .venv/bin/activate        # Linux/Mac
# .venv\Scripts\activate         # Windows

# Bağımlılıkları yükle
pip install -r requirements.txt

# Yerel PostgreSQL (isteğe bağlı): docker compose up -d
# .env dosyasını oluştur
cp .env.example .env
# .env içinde SECRET_KEY ve DB_* değerlerini düzenle (DB_* geliştirme ve üretimde zorunlu)

# Veritabanını oluştur
python manage.py migrate

# Superuser oluştur (admin paneli için)
python manage.py createsuperuser

# Statik dosyaları topla (production'da gerekli)
python manage.py collectstatic --noinput

# Geliştirme sunucusunu başlat
python manage.py runserver
```

---

## 2. requirements.txt

Gerçek dosya `requirements.txt` ile aynı tutun; özet:

```txt
# Django Core
Django>=5.0,<6.0

# DTO / validation
pydantic>=2,<3
Pillow>=10.0          # ImageField

# Veritabanı
psycopg2-binary>=2.9  # PostgreSQL

# Environment
python-decouple>=3.8

# Statik dosya (production)
whitenoise>=6.6

# WSGI (Docker / production)
gunicorn>=22.0

# Önbellek (modulith: Redis)
django-redis>=5.4
redis>=5.0

# Geliştirme (opsiyonel)
django-debug-toolbar>=4.0
```

---

## Docker ile çalıştırma

### Geliştirme (yerel tam yığın)

Proje kökünde `Dockerfile`; `docker-compose.yml` PostgreSQL 16, Redis 7 ve Gunicorn ile `web` servisini başlatır.

```bash
cd storium-modulith
docker compose up --build
```

- Uygulama: varsayılan `http://localhost:8001` (`.env` ile `DOCKER_WEB_PORT` değiştirilebilir; 8000/5432 meşgul senaryoları için)
- Ortam değişkenleri `docker-compose.yml` içinde tanımlıdır (`DJANGO_ENV=development`, `DB_*`, `REDIS_URL`, `DJANGO_SIMPLE_STATIC=true`).

Süper kullanıcı:

```bash
docker compose run --rm web python manage.py createsuperuser
```

Örnek katalog verisi: `web` konteyneri ayağa kalkarken `DJANGO_RUN_SEED=true` ile otomatik çalışır (`docker-compose.yml`). İsterseniz elle:

```bash
docker compose run --rm web python manage.py seed_catalog
docker compose run --rm web python manage.py seed_catalog --with-demo-user
```

### Üretim (docker-compose.prod.yml)

1. `.env.production.example` dosyasını `.env.production` olarak kopyalayın; `SECRET_KEY`, `DB_*`, `ALLOWED_HOSTS` ve e-posta (SMTP) alanlarını doldurun.
2. Aşağıdaki komutta `--env-file .env.production` kullanın; böylece hem `db` servisinin `POSTGRES_*` değişkenleri hem `web` için Django ayarları aynı dosyadan okunur.

```bash
docker compose --env-file .env.production -f docker-compose.prod.yml up -d --build
```

TLS terminasyonu reverse proxy’deyse ve konteynıra düz HTTP geliyorsa, geçici olarak `.env.production` içinde `SECURE_SSL_REDIRECT=false` (ve gerekirse `SESSION_COOKIE_SECURE` / `CSRF_COOKIE_SECURE`) kullanılabilir. İnternete açık ortamda TLS ve uygun proxy başlıkları ile güvenli varsayılanlar (`true`) korunmalıdır.

---

## 3. Django Proje Başlatma Komutu

```bash
# Proje iskeletini oluştur (storium-modulith/ içinde)
django-admin startproject storium .

# App'leri oluştur
mkdir -p apps
python manage.py startapp catalog apps/catalog
python manage.py startapp cart apps/cart
python manage.py startapp orders apps/orders
python manage.py startapp notifications apps/notifications

# Core dizinlerini oluştur
mkdir -p core/repositories core/services core/dtos core/exceptions
touch core/__init__.py core/repositories/__init__.py core/services/__init__.py
touch core/dtos/__init__.py core/exceptions/__init__.py
```

---

## 4. Settings Yapısı

### storium/settings/\_\_init\_\_.py
```python
import os
from decouple import config

DJANGO_ENV = config('DJANGO_ENV', default='development')

if DJANGO_ENV == 'production':
    from .production import *
else:
    from .development import *
```

### storium/settings/base.py (Ortak Ayarlar)

```python
from pathlib import Path
from decouple import config

BASE_DIR = Path(__file__).resolve().parent.parent.parent

SECRET_KEY = config('SECRET_KEY')

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Proje app'leri
    'modules.catalog',
    'modules.cart',
    'modules.orders',
    'modules.notifications',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',     # WhiteNoise (statik dosya)
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'storium.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                # Sepet sayacı — tüm template'lere cart_item_count ekler
                'modules.cart.context_processors.cart_context',
                'modules.catalog.context_processors.catalog_nav',
            ],
        },
    },
]

WSGI_APPLICATION = 'storium.wsgi.application'

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'tr-tr'
TIME_ZONE = 'Europe/Istanbul'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_URL = '/giris/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

# Django Messages → Bootstrap renk eşleşmesi
from django.contrib.messages import constants as msg
MESSAGE_TAGS = {
    msg.DEBUG:   'secondary',
    msg.INFO:    'info',
    msg.SUCCESS: 'success',
    msg.WARNING: 'warning',
    msg.ERROR:   'danger',
}
```

### storium/settings/development.py

```python
from .base import *
from decouple import config

DEBUG = True
ALLOWED_HOSTS = ['localhost', '127.0.0.1']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST', default='localhost'),
        'PORT': config('DB_PORT', default='5432'),
    }
}

# E-postalar terminale yazılır
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
DEFAULT_FROM_EMAIL = 'noreply@storium.local'

# Debug toolbar (opsiyonel — INSTALLED_APPS'e de eklenmeli)
# INSTALLED_APPS += ['debug_toolbar']
# MIDDLEWARE.insert(0, 'debug_toolbar.middleware.DebugToolbarMiddleware')
# INTERNAL_IPS = ['127.0.0.1']
```

### storium/settings/production.py

```python
from .base import *
from decouple import config

DEBUG = False
ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=lambda v: [h.strip() for h in v.split(',')])

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST', default='localhost'),
        'PORT': config('DB_PORT', default='5432'),
    }
}

# SMTP E-posta
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = config('EMAIL_HOST')
EMAIL_PORT = config('EMAIL_PORT', cast=int, default=587)
EMAIL_USE_TLS = True
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL', default='noreply@storium.com')

SECURE_HSTS_SECONDS = 31536000
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
```

---

## 5. Docker ile yerel çalıştırma (Django + PostgreSQL)

Proje kökünde `Dockerfile`, `docker-entrypoint.sh` ve `docker-compose.yml` bulunur: **web** (Gunicorn) + **db** (Postgres 16) + **redis** (önbellek). Konteyner içinde `DB_HOST=db` ve `REDIS_URL=redis://redis:6379/1` kullanılır.

```bash
cd storium-modulith
# İsteğe bağlı: proje kökünde .env içinde SECRET_KEY=... (compose ${SECRET_KEY} ile okur)
docker compose up --build
```

- Uygulama: **http://localhost:8000**
- İlk kurulumda süper kullanıcı: `docker compose run --rm -it web python manage.py createsuperuser`
- Yalnızca veritabanı (host’tan `runserver`): `docker compose up -d db` — `.env` içinde `DB_HOST=localhost` kullanın.

`docker-entrypoint.sh`: Postgres hazır olana kadar bekler, `migrate` ve `collectstatic` çalıştırır; yüklenen görseller `storium_media` volume’unda kalır.

### Bağlantı reddedildi (`ERR_CONNECTION_REFUSED`)

Bu hata, tarayıcının bağlandığı adreste **hiçbir süreç dinlemiyor** demektir (çoğunlukla `http://localhost:8000`).

1. **Docker ile çalıştırıyorsanız:** Windows’ta **Docker Desktop**’ı açın (sistem tepsisinde Docker çalışır olmalı). Proje kökünde: `docker compose up --build`. Ardından `docker compose ps` — `web` **running** ve **healthy** (veya en azından Up) olmalı. Hata varsa: `docker compose logs web` (Gunicorn / migrate / collectstatic çıktısı).
2. **Yerel `runserver` kullanıyorsanız:** PostgreSQL ayakta olmalı (ör. `docker compose up -d db` veya yerel kurulum), `.env` dolu olmalı; sonra `python manage.py runserver` — terminal kapanırsa sunucu da durur.
3. Port çakışması: Başka bir uygulama 8000 kullanıyorsa `python manage.py runserver 8080` veya compose’ta `"8080:8000"` kullanın.

**Windows:** `docker-entrypoint.sh` satır sonları CRLF ise konteyner hemen çıkabilir; güncel `Dockerfile` içinde `sed` ile düzeltilir — imajı yeniden derleyin: `docker compose build --no-cache web`.

## 6. .env.example

```env
# Django
DJANGO_ENV=development
SECRET_KEY=your-very-secret-key-change-this

# PostgreSQL (development ve production — django.db.backends.postgresql)
DB_NAME=storium_db
DB_USER=storium_user
DB_PASSWORD=storium_password
DB_HOST=localhost
DB_PORT=5432

# Redis (modulith önbellek). Boş = LocMem. Örnek: redis://localhost:6379/1
REDIS_URL=

# Production host (sadece DJANGO_ENV=production iken kullanılır)
ALLOWED_HOSTS=storium.com,www.storium.com

# E-posta (production)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=noreply@storium.com
```

---

## 7. .gitignore

```gitignore
# Python
__pycache__/
*.py[cod]
*.pyo
.venv/
venv/
env/

# Django
*.log
local_settings.py
db.sqlite3
media/
staticfiles/

# Environment
.env

# IDE
.vscode/
.idea/
*.swp
```

---

## 8. storium/urls.py (Ana URL Dosyası)

```python
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),

    # Auth
    path('giris/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('cikis/', auth_views.LogoutView.as_view(), name='logout'),

    # Uygulama
    path('', include('modules.catalog.urls', namespace='catalog')),
    path('', include('modules.cart.urls', namespace='cart')),
    path('siparis/', include('modules.orders.urls', namespace='orders')),
]

# Development'ta media dosyaları serve et
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

---

## 9. Makefile (Opsiyonel — Kısa Yol Komutları)

```makefile
.PHONY: run migrate shell test

run:
	python manage.py runserver

migrate:
	python manage.py makemigrations
	python manage.py migrate

shell:
	python manage.py shell

test:
	python manage.py test

superuser:
	python manage.py createsuperuser

static:
	python manage.py collectstatic --noinput

reset-db:
	python manage.py flush --noinput
	python manage.py migrate
	python manage.py createsuperuser
```

---

## 10. Örnek Veri

### Komut ile seed (önerilir)

```bash
python manage.py seed_catalog
# İsteğe bağlı test kullanıcısı (kullanıcı: demo, şifre: storium-demo-2024):
python manage.py seed_catalog --with-demo-user
```

Kök kategoriler: Elektronik, Ev ve Yaşam, Kitap; alt kategori ve 8 örnek ürün. Tekrar çalıştırıldığında `get_or_create` ile güncellenir.

### Admin panel ile manuel

```
1. python manage.py createsuperuser
2. http://localhost:8000/admin/ → Giriş yap
3. Catalog > Categories → Kategori ekle (slug otomatik dolar)
4. Catalog > Products → Ürün ekle, kategori seç, görsel yükle
5. http://localhost:8000/ → Anasayfayı görüntüle
```

Docker: `docker compose run --rm web python manage.py seed_catalog`

---

## 11. Doğrulama Checklist

```
✓ http://localhost:8000/              → Ana sayfa açılıyor
✓ http://localhost:8000/kategori/elektronik/  → Ürün listesi (slug ile)
✓ http://localhost:8000/urun/laptop/          → Ürün detay
✓ http://localhost:8000/arama/?q=laptop       → Arama sonuçları
✓ Sepete Ekle butonu çalışıyor
✓ http://localhost:8000/sepet/                → Sepet sayfası
✓ Sepette miktar güncelleme ve silme çalışıyor
✓ http://localhost:8000/giris/               → Login sayfası
✓ http://localhost:8000/siparis/checkout/    → Checkout (login gerekli)
✓ Sipariş tamamlandıktan sonra e-posta terminalde görünüyor (console backend)
✓ http://localhost:8000/siparis/             → Sipariş listesi
✓ http://localhost:8000/admin/               → Admin paneli
```
