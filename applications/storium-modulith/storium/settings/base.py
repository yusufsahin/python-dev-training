import sys
from pathlib import Path

from decouple import config

BASE_DIR = Path(__file__).resolve().parent.parent.parent

SECRET_KEY = config("SECRET_KEY")

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "modules.catalog",
    "modules.cart",
    "modules.orders",
    "modules.notifications",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "storium.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "modules.cart.context_processors.cart_context",
                "modules.catalog.context_processors.catalog_nav",
            ],
        },
    },
]

WSGI_APPLICATION = "storium.wsgi.application"

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "tr-tr"
TIME_ZONE = "Europe/Istanbul"
USE_I18N = True
USE_TZ = True

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "static"]
# Docker / CI: manifest bazen eksik hash ile kırılır; DJANGO_SIMPLE_STATIC=true → Manifest kullanılmaz
if config("DJANGO_SIMPLE_STATIC", default=False, cast=bool):
    STATICFILES_STORAGE = "whitenoise.storage.CompressedStaticFilesStorage"
else:
    STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Önbellek: REDIS_URL tanımlıysa Redis (django-redis), yoksa yerel LocMem.
# manage.py test: LocMem testler arası sızmasın diye DummyCache.
REDIS_URL = config("REDIS_URL", default="").strip()
if "test" in sys.argv:
    CACHES = {
        "default": {"BACKEND": "django.core.cache.backends.dummy.DummyCache"},
    }
elif REDIS_URL:
    CACHES = {
        "default": {
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": REDIS_URL,
            "OPTIONS": {
                "CLIENT_CLASS": "django_redis.client.DefaultClient",
            },
            "KEY_PREFIX": "storium_mod",
        }
    }
else:
    CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
            "LOCATION": "storium-modulith",
        }
    }

LOGIN_URL = "/giris/"
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"

SESSION_COOKIE_AGE = 1209600

from django.contrib.messages import constants as msg  # noqa: E402

MESSAGE_TAGS = {
    msg.DEBUG: "secondary",
    msg.INFO: "info",
    msg.SUCCESS: "success",
    msg.WARNING: "warning",
    msg.ERROR: "danger",
}
