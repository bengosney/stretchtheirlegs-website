# Standard Library

# Django
from django.db import models

# Wagtail
from wagtail.admin.panels import FieldPanel, MultiFieldPanel

# First Party
from fh_utils.models import statusDatePeriodMixin, statusMixin


class Banner(statusDatePeriodMixin, models.Model):
    image = models.ForeignKey("wagtailimages.Image", null=True, blank=True, on_delete=models.SET_NULL, related_name="+")

    panels = [
        *statusMixin.mixin_panels,
        MultiFieldPanel(
            [
                FieldPanel("show_from"),
                FieldPanel("show_to"),
            ],
            heading="Date Range",
        ),
        FieldPanel("image"),
    ]

    class Meta:
        default_manager_name = "admin_objects"

    @classmethod
    def get_current_image(cls):
        try:
            image = cls.objects.all().order_by("show_from")[0]
        except IndexError:
            image = None

        return image
