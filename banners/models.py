# Django
from django.contrib import admin
from django.db import models
from django.forms.utils import flatatt
from django.utils.html import mark_safe

# Wagtail
from wagtail.admin.panels import FieldPanel, FieldRowPanel

# First Party
from fh_utils.models import statusDatePeriodMixin, statusMixin


class Banner(statusDatePeriodMixin, models.Model):
    image = models.ForeignKey("wagtailimages.Image", null=True, blank=True, on_delete=models.SET_NULL, related_name="+")

    panels = (
        *statusMixin.mixin_panels,
        FieldRowPanel(
            [
                FieldPanel("show_from"),
                FieldPanel("show_to"),
            ],
            heading="Date Range",
        ),
        FieldPanel("image"),
    )

    class Meta:
        default_manager_name = "admin_objects"

    def __str__(self) -> str:
        return str(self.image) if self.image else "No Image"

    @classmethod
    def get_current_image(cls):
        try:
            image = cls.objects.all().order_by("show_from")[0]
        except IndexError:
            image = None

        return image

    @admin.display(description="preview")
    def admin_preview(self) -> str:
        if not self.image:
            return ""

        WIDTH = 50

        rendition = self.image.get_rendition(f"width-{WIDTH}")
        img_attrs = {
            "src": rendition.url,
            "width": WIDTH,
            "decoding": "async",
            "loading": "lazy",
        }

        return mark_safe(f"<img{flatatt(img_attrs)}>")
