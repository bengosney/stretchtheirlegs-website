from typing import ClassVar

from django.contrib import admin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, Panel

from fh_utils import ModelStatus
from fh_utils.exceptions import PublishedDateValidationError
from fh_utils.fields import DayMonthField
from fh_utils.managers import DateManager, DatePeriodManager, DateRangeManager, StatusManager


class StatusMixin(models.Model):
    status = models.IntegerField(_("Status"), choices=ModelStatus.STATUS_CHOICES, default=ModelStatus.LIVE_STATUS)

    admin_objects = models.Manager()
    objects = StatusManager()

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.status}"

    @property
    @admin.display(description="status")
    def status_name(self) -> str:
        return ModelStatus.get_name(self.status)

    mixin_panels: ClassVar[list[Panel]] = [FieldPanel("status")]


class StatusDatePeriodMixin(StatusMixin):
    show_from = DayMonthField(_("Show From"))
    show_to = DayMonthField(_("Show To"), after="show_from")

    objects = type("statusSatePeriodManager", (StatusManager, DatePeriodManager), {})()

    class Meta:
        abstract = True

    @property
    @admin.display(description="show from")
    def admin_show_from(self) -> str:
        return self.show_from.strftime("%B %d")

    @property
    @admin.display(description="show to")
    def admin_show_to(self) -> str:
        return self.show_to.strftime("%B %d")

    mixin_panels: ClassVar[list[MultiFieldPanel]] = [
        MultiFieldPanel(
            [*StatusMixin.mixin_panels, FieldPanel("show_from"), FieldPanel("show_to")],
            heading=_("Date Range"),
        ),
    ]


class StatusDateMixin(StatusMixin):
    published = models.DateField(_("Published"))

    objects = type("statusDateManager", (StatusManager, DateManager), {})()

    class Meta:
        abstract = True

    mixin_panels: ClassVar[list[MultiFieldPanel]] = [
        MultiFieldPanel(
            [*StatusMixin.mixin_panels, FieldPanel("published")],
            heading=_("Published"),
        ),
    ]


class StatusDateRangeMixin(StatusMixin):
    published_from = models.DateField(_("Published from"))
    published_to = models.DateField(_("Published to"))

    objects = type("statusDateRangeManager", (StatusManager, DateRangeManager), {})()

    class Meta:
        abstract = True

    mixin_panels: ClassVar[list[MultiFieldPanel]] = [
        MultiFieldPanel(
            [*StatusMixin.mixin_panels, FieldPanel("published_from"), FieldPanel("published_to")],
            heading=_("Published"),
        ),
    ]

    def save(self, *args, **kwargs):
        self._validate_start_end_dates()
        return super().save(*args, **kwargs)

    @property
    def has_passed(self):
        return self.published_from < timezone.now().date()

    def _validate_start_end_dates(self):
        if self.published_to < self.published_from:
            raise PublishedDateValidationError(self.published_from, self.published_to)
