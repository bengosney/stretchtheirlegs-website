# Standard Library
from datetime import datetime

# Django
from django.db import models
from django.db.models import Q

# Locals
from . import ModelStatus
from .fields import DayMonthField


class statusManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=ModelStatus.LIVE_STATUS)


class datePeriodManager(models.Manager):
    @staticmethod
    def _get_q():
        today = datetime.now().replace(year=DayMonthField.get_base_year())
        nextYear = today.replace(year=today.year + 1)

        return Q(show_from__lte=today, show_to__gte=today) | Q(show_from__lte=nextYear, show_to__gte=nextYear)

    def get_queryset(self):

        return (
            super()
            .get_queryset()
            .filter(self._get_q())
        )


class dateManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(published__lte=datetime.now())


class dateRangeManager(models.Manager):
    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(
                published_from__lte=datetime.now(),
                published_to__gte=datetime.now(),
            )
        )
