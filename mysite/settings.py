"""
Django settings for mysite project.
"""

import os
from pathlib import Path
import environ

# Định nghĩa BASE_DIR
BASE_DIR = Path(__file__).resolve().parent.parent

# Khởi tạo env
env = environ.Env(
    DEBUG=(bool, False)
)

# Load file .env nếu tồn tại (local dev)
environ.Env.read_env(os.path.join(BASE_DIR, ".env"))

# Cấu hình bảo mật
SECRET_KEY = env("SECRET_KEY", default="dev-fallback-secret-key")
DEBUG = env.bool("DEBUG", default=False)
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=["127.0.0.1", "localhost"])

# Nếu deploy thì ALLOWED_HOSTS = ['*'] để Render tự bind
if not DEBUG:
    ALLOWED_HOSTS = ["*"]

# Static
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

# Media
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "mediafiles"

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# Ứng dụng
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.humanize",
    "product",
    "widget_tweaks",
]

# Middleware
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",   # ✅ để phục vụ static trên Render
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "mysite.urls"

# Templates
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "mysite.wsgi.application"

# Database (SQLite mặc định, có thể override bằng DATABASE_URL khi deploy)
DATABASES = {
    "default": env.db(default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}")
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# Auth redirects
LOGIN_REDIRECT_URL = "/products/"
LOGOUT_REDIRECT_URL = "/products/login/"
LOGIN_URL = "login"

# I18N
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# Default primary key
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
