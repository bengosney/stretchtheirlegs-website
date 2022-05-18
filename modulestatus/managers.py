# Standard Library
from datetime import datetime

# Django
from django.db import models

# Locals
from . import ModelStatus


class statusManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=ModelStatus.LIVE_STATUS)


class statusDateManager(statusManager):
    def get_queryset(self):
        return super().get_queryset().filter(published__lte=datetime.now().date())


class statusDateRangeManager(statusManager):
    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(
                published_from__lte=datetime.today().date(),
                published_to__gte=datetime.today().date(),
            )
        )
