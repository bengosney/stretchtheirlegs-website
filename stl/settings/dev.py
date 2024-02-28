# Standard Library
import os

# First Party
from stl.settings.base import *  # noqa
from stl.settings.base import INSTALLED_APPS, MIDDLEWARE, PROJECT_DIR, STATICFILES_DIRS

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-5y%vys$7ftzwnthn@ud8vl&=w#9d)b1%i8r(6d2b35!jt+uf^3"

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ["*"]

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"


INSTALLED_APPS += [
    "debug_toolbar",
    "debugtools",
]

MIDDLEWARE += [
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

CSRF_TRUSTED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

SCSS_SOURCEMAP_URL = "/scss/"
SCSS_SOURCEMAP_ROOT = os.path.join(PROJECT_DIR, "..", "scss")

STATICFILES_DIRS += [
    os.path.join(PROJECT_DIR, "..", "scss"),
]

try:
    # First Party
    from stl.settings.local import *  # noqa
except ImportError:
    pass
