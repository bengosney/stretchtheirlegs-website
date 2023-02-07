# Django
from django.db import models
from django.utils.translation import gettext_lazy as _

# Wagtail
from wagtail.admin.panels import FieldPanel, MultiFieldPanel

# First Party
from fh_utils.models import statusDatePeriodMixin, statusMixin


class Logo(statusDatePeriodMixin, models.Model):
    title = models.TextField(_("Title"))
    logo = models.FileField(_("Logo SVG"), upload_to="logos")
    fireworks = models.BooleanField(_("Show fireworks"), default=False)
    snow = models.BooleanField(_("Show snow"), default=False)

    panels = [
        *statusMixin.mixin_panels,
        MultiFieldPanel(
            [
                FieldPanel("show_from"),
                FieldPanel("show_to"),
            ],
            heading="Date Range",
        ),
        MultiFieldPanel(
            [
                FieldPanel("title"),
                FieldPanel("logo"),
            ],
            heading="Details",
        ),
        MultiFieldPanel(
            [
                FieldPanel("fireworks"),
                FieldPanel("snow"),
            ],
            heading="Effects",
        ),
    ]

    class Meta:
        default_manager_name = "admin_objects"

    def __str__(self):
        return self.title

    @property
    def svg(self) -> str:
        try:
            return self.logo.read().decode("utf-8")
        except FileNotFoundError:
            return ""

    @classmethod
    def get_current_logo(cls):
        try:
            return cls.objects.all().order_by("show_from")[0]
        except IndexError:
            return None
