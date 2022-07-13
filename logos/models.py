# Django
from django.db import models
from django.utils.translation import gettext_lazy as _

# Wagtail
from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel

# First Party
from fh_utils.models import statusDatePeriodMixin, statusMixin


class Logo(statusDatePeriodMixin, models.Model):
    title = models.TextField(_("Title"))
    logo = models.FileField(_("Logo SVG"), upload_to="logos")

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
            ]
        ),
    ]

    class Meta:
        default_manager_name = "admin_objects"

    @property
    def svg(self) -> str:
        return self.logo.read().decode("utf-8")

    @classmethod
    def get_current_logo(cls):
        try:
            return cls.objects.all().order_by("show_from")[0]
        except IndexError:
            return None
