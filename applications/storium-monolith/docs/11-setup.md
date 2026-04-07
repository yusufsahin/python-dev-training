# 11 — Kurulum ve Konfigürasyon

## Ön Gereksinimler
- Python 3.12+
- pip
- Git

---

## 1. Proje Kurulumu

```bash
# Çalışma dizinine git
cd storium-monolith

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

```txt
# Core
Django>=5.0,<6.0
Pillow>=10.0          # ImageField için

# Veritabanı (development + production)
psycopg2-binary>=2.9  # PostgreSQL driver

# Environment
python-decouple>=3.8  # .env okuma (veya django-environ)

# Statik dosya (production)
whitenoise>=6.6

# Geliştirme araçları (opsiyonel)
django-debug-toolbar>=4.0
```

---

## 3. Django Proje Başlatma Komutu

```bash
# Proje iskeletini oluştur (storium-monolith/ içinde)
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
    'apps.catalog',
    'apps.cart',
    'apps.orders',
    'apps.notifications',
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
                'apps.cart.context_processors.cart_context',
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

## 5. Yerel PostgreSQL (Docker Compose, isteğe bağlı)

Proje köküne `docker-compose.yml` ekleyebilirsiniz:

```yaml
services:
  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_USER: storium_user
      POSTGRES_PASSWORD: storium_password
      POSTGRES_DB: storium_db
    ports:
      - "5432:5432"
    volumes:
      - storium_pgdata:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U storium_user -d storium_db"]
      interval: 5s
      timeout: 5s
      retries: 5

volumes:
  storium_pgdata:
```

```bash
docker compose up -d
# Ardından .env içindeki DB_* değerleri compose ile aynı olmalı
python manage.py migrate
```

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
    path('', include('apps.catalog.urls', namespace='catalog')),
    path('', include('apps.cart.urls', namespace='cart')),
    path('siparis/', include('apps.orders.urls', namespace='orders')),
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

## 10. Örnek Veri (Admin Panel ile)

```
1. python manage.py createsuperuser
2. http://localhost:8000/admin/ → Giriş yap
3. Catalog > Categories → Kategori ekle (slug otomatik dolar)
4. Catalog > Products → Ürün ekle, kategori seç, görsel yükle
5. http://localhost:8000/ → Anasayfayı görüntüle
```

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
