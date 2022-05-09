# Standard Library
from datetime import datetime

# Django
from django.db import models

# Wagtail
from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel

# Third Party
from icecream import ic

# First Party
from modulestatus.models import statusMixin


class Banner(statusMixin, models.Model):
    show_from = models.DateField()
    show_to = models.DateField()

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
        ImageChooserPanel("image"),
    ]

    @classmethod
    def getCurrentImage(cls):
        today = datetime.now()

        ic(today)

        try:
            image = cls.objects.filter(
                show_from__month__lte=today.month,
                show_from__day__lte=today.day,
                show_to__month__gte=today.month,
                show_to__day__gte=today.day,
            )[0]
        except IndexError:
            image = None

        return image
