from .base import *  # noqa: F403
import os

SECRET_KEY = (
    "django-insecure-73t7!or6gd%r+tc5#%0l*5a45*lm=x3os80@i%003$wr_zj^_5"
)
DEBUG = True

ALLOWED_HOSTS = []


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

INSTALLED_APPS += ("debug_toolbar",)
MIDDLEWARE = [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
] + MIDDLEWARE
INTERNAL_IPS = ("127.0.0.1", "localhost")

DJANGO_TEMPLATES["APP_DIRS"] = True

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "file": {
            "level": "DEBUG",
            "class": "logging.FileHandler",
            "filename": "/Users/jammon/workspace/stationsplan/debug.log",
        },
    },
    "loggers": {
        "django.request": {
            "handlers": ["file"],
            "level": "DEBUG",
            "propagate": True,
        },
    },
}
