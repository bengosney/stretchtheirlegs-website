# Standard Library
import contextlib
import os

# Third Party
import dj_database_url

# Locals
from .base import *  # noqa

DEBUG = False

env = os.environ.copy()

AWS_ACCESS_KEY_ID = env["AWS_ACCESS_KEY_ID"]
AWS_SECRET_ACCESS_KEY = env["AWS_SECRET_ACCESS_KEY"]
AWS_STORAGE_BUCKET_NAME = env["AWS_STORAGE_BUCKET_NAME"]
AWS_QUERYSTRING_AUTH = False
AWS_S3_CUSTOM_DOMAIN = env["AWS_S3_CUSTOM_DOMAIN"]
AWS_LOCATION = env["AWS_LOCATION"] if "AWS_LOCATION" in env else ""
AWS_S3_OBJECT_PARAMETERS = {
    "CacheControl": f"max-age={86400 * 365}",
}

ALLOWED_HOSTS = ["www.stretchtheirlegs.co.uk"]

CSRF_TRUSTED_ORIGINS = [
    BASE_URL,  # noqa
]

DATABASES["default"] = dj_database_url.config()  # noqa

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

SECRET_KEY = env["SECRET_KEY"]

STORAGES = {
    "default": {
        "BACKEND": "storages.backends.s3boto3.S3Boto3Storage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

MIDDLEWARE += [  # noqa
    "whitenoise.middleware.WhiteNoiseMiddleware",
]

COMPRESS_OFFLINE = True
COMPRESS_CSS_FILTERS = [
    "compressor.filters.css_default.CssAbsoluteFilter",
    "compressor.filters.cssmin.CSSMinFilter",
]
COMPRESS_CSS_HASHING_METHOD = "content"


with contextlib.suppress(KeyError):
    HONEYBADGER = {"API_KEY": env["HONEYBADGER_API_KEY"]}
    MIDDLEWARE = [
        "honeybadger.contrib.DjangoHoneybadgerMiddleware",
    ] + MIDDLEWARE

WAGTAILIMAGES_FEATURE_DETECTION_ENABLED = True

with contextlib.suppress(KeyError):
    EMAIL_HOST = env["SMTP_HOST"]
    EMAIL_HOST_USER = env["SMTP_USER"]
    EMAIL_HOST_PASSWORD = env["SMTP_PASS"]
    EMAIL_PORT = env["SMTP_PORT"]
    EMAIL_USE_TLS = True
    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"


CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "default",
    },
    "renditions": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "renditions",
    },
}

if "REDIS_URL" in os.environ:
    REDIS_URL = os.environ.get("REDIS_URL")
    CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.redis.RedisCache",
            "LOCATION": REDIS_URL,
        },
        "renditions": {
            "BACKEND": "django.core.cache.backends.redis.RedisCache",
            "LOCATION": REDIS_URL,
        },
    }


with contextlib.suppress(ImportError):
    # Locals
    from .local import *  # noqa
