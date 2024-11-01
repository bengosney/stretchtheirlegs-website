from typing import ClassVar

from django.contrib import admin
from django.db import models
from django.forms.utils import flatatt
from django.utils.html import mark_safe

from wagtail.admin.panels import FieldPanel, FieldRowPanel, Panel

from fh_utils.models import StatusDatePeriodMixin, StatusMixin


class Banner(StatusDatePeriodMixin, models.Model):
    image = models.ForeignKey("wagtailimages.Image", null=True, blank=True, on_delete=models.SET_NULL, related_name="+")

    panels: ClassVar[list[Panel]] = [
        *StatusMixin.mixin_panels,
        FieldRowPanel(
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

    def __str__(self):
        return f"{self.image.title}" if self.image else "No Image"

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

        width = 50

        rendition = self.image.get_rendition(f"width-{width}")
        img_attrs = {
            "src": rendition.url,
            "width": width,
            "decoding": "async",
            "loading": "lazy",
        }

        return mark_safe(f"<img{flatatt(img_attrs)}>")
