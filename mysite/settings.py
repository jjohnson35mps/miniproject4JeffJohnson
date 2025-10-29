### INF601 - Advanced Programming in Python
### Jeff Johnson
### Mini Project 4

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = "replace-this-with-your-own-secret-key"

DEBUG = True

ALLOWED_HOSTS = []  # during development


# Application definition
INSTALLED_APPS = [
    "django.contrib.admin",        # admin site
    "django.contrib.auth",         # auth system (login/logout)
    "django.contrib.contenttypes", # content type framework
    "django.contrib.sessions",     # session framework
    "django.contrib.messages",     # messaging framework
    "django.contrib.staticfiles",  # static files handling
    "polls",                       # our app from tutorial parts 1–8
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",  # enables request.user
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "mysite.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        # By default, DIRS can point to global template dirs.
        "DIRS": [],
        # APP_DIRS=True means: also look in each INSTALLED_APP for templates/
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "mysite.wsgi.application"
ASGI_APPLICATION = "mysite.asgi.application"


# Database (SQLite default)
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True


# Static files (tutorial part 6)
STATIC_URL = "static/"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Send users to the home page after login/logout instead of /accounts/profile/
LOGIN_REDIRECT_URL = '/'
ACCOUNT_LOGOUT_ON_GET = True
LOGOUT_REDIRECT_URL = '/'
