"""
Django settings for mandel_lotto project.
"""

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# Security
SECRET_KEY = os.environ.get(
    "DJANGO_SECRET_KEY",
    "dev-only-change-in-production"
)

DEBUG = os.environ.get("DJANGO_DEBUG", "1") == "1"

# Railway / Hosts
ALLOWED_HOSTS = ["*"]

CSRF_TRUSTED_ORIGINS = [
    "https://*.up.railway.app",
]

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# Applications
INSTALLED_APPS = [
    "django.contrib.contenttypes",
    "django.contrib.staticfiles",

    "analyzer.apps.AnalyzerConfig",
]

# Middleware
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",

    "whitenoise.middleware.WhiteNoiseMiddleware",

    "django.middleware.common.CommonMiddleware",

    "django.middleware.csrf.CsrfViewMiddleware",

    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# URLs / WSGI
ROOT_URLCONF = "mandel_lotto.urls"

WSGI_APPLICATION = "mandel_lotto.wsgi.application"

# Templates
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",

        "DIRS": [BASE_DIR / "templates"],

        "APP_DIRS": True,

        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
            ],
        },
    },
]

# Database
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# Internationalization
LANGUAGE_CODE = "he"

TIME_ZONE = "Asia/Jerusalem"

USE_I18N = True

USE_TZ = True

# Static files
STATIC_URL = "/static/"

STATIC_ROOT = BASE_DIR / "staticfiles"

STATICFILES_DIRS = (
    [BASE_DIR / "static"]
    if (BASE_DIR / "static").exists()
    else []
)

STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedStaticFilesStorage",
    },
}

# Default primary key
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Data directory
DATA_DIR = BASE_DIR / "data"