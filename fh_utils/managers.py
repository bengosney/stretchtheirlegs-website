# Standard Library
from datetime import datetime

# Django
from django.db import models
from django.db.models import Q

# First Party
from fh_utils import ModelStatus
from fh_utils.fields import DayMonthField


class StatusManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=ModelStatus.LIVE_STATUS)


class DatePeriodManager(models.Manager):
    @staticmethod
    def _get_q():
        today = datetime.now().replace(year=DayMonthField.get_base_year())
        next_year = today.replace(year=today.year + 1)

        return Q(show_from__lte=today, show_to__gte=today) | Q(show_from__lte=next_year, show_to__gte=next_year)

    def get_queryset(self):
        return super().get_queryset().filter(self._get_q())


class DateManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(published__lte=datetime.now())


class DateRangeManager(models.Manager):
    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(
                published_from__lte=datetime.now(),
                published_to__gte=datetime.now(),
            )
        )
