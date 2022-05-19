# Django
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

# Wagtail
from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel

# Locals
from . import ModelStatus
from .fields import DayMonthField
from .managers import dateManager, datePeriodManager, dateRangeManager, statusManager


class statusMixin(models.Model):
    status = models.IntegerField(_("Status"), choices=ModelStatus.STATUS_CHOICES, default=ModelStatus.LIVE_STATUS)

    objects = statusManager()
    admin_objects = models.Manager()

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.status}"

    mixin_panels = [
        FieldPanel("status"),
    ]


class statusDatePeriodMixin(statusMixin):
    show_from = DayMonthField(_("Show From"))
    show_to = DayMonthField(_("Show To"), after="show_from")

    objects = type("statusSatePeriodManager", (statusManager, datePeriodManager), {})()

    class Meta:
        abstract = True

    mixin_panels = [
        MultiFieldPanel(
            statusMixin.mixin_panels
            + [
                FieldPanel("show_from"),
                FieldPanel("show_to"),
            ],
            heading=_("Date Range"),
        ),
    ]


class statusDateMixin(statusMixin):
    published = models.DateField(_("Published"))

    objects = type("statusDateManager", (statusManager, dateManager), {})()

    class Meta:
        abstract = True

    mixin_panels = [
        MultiFieldPanel(
            statusMixin.mixin_panels
            + [
                FieldPanel("published"),
            ],
            heading=_("Published"),
        ),
    ]


class statusDateRangeMixin(statusMixin):
    published_from = models.DateField(_("Published from"))
    published_to = models.DateField(_("Published to"))

    objects = type("statusDateRangeManager", (statusManager, dateRangeManager), {})()

    class Meta:
        abstract = True

    mixin_panels = [
        MultiFieldPanel(
            statusMixin.mixin_panels
            + [
                FieldPanel("published_from"),
                FieldPanel("published_to"),
            ],
            heading=_("Published"),
        ),
    ]

    @property
    def has_passed(self):
        return self.published_from < timezone.now()
