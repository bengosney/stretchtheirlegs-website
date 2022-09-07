# Locals
from .base import *  # noqa

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-5y%vys$7ftzwnthn@ud8vl&=w#9d)b1%i8r(6d2b35!jt+uf^3"

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ["*"]

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"


INSTALLED_APPS += [  # noqa
    "debug_toolbar",
    "debugtools",
]

MIDDLEWARE += [  # noqa
    "debug_toolbar.middleware.DebugToolbarMiddleware",
]

INTERNAL_IPS = [
    "127.0.0.1",
]

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "incremental": True,
    "root": {
        "level": "DEBUG",
    },
}

CSP_DEFAULT_SRC = None
CSP_STYLE_SRC = None
CSP_FONT_SRC = None
CSP_IMG_SRC = None

CORS_ALLOWED_ORIGINS = [
    "https://cerberus.stretchtheirlegs.co.uk",
]

try:
    # Locals
    from .local import *  # noqa
except ImportError:
    pass
