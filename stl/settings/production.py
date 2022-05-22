# Locals
from .base import *  # noqa

DEBUG = False

INSTALLED_APPS += [  # noqa
    "health_check.contrib.migrations",
    "health_check.contrib.psutil",
    "health_check.contrib.s3boto3_storage",
    "health_check.contrib.redis",
    "health_check.db",
]

try:
    # Locals
    from .local import *  # noqa
except ImportError:
    pass
