# Standard Library
from datetime import datetime

# Django
from django.db import models
from django.db.models import Q

# Wagtail
from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel

# First Party
from fh_utils.fields import DayMonthField
from fh_utils.models import statusMixin


class Banner(statusMixin, models.Model):
    show_from = DayMonthField()
    show_to = DayMonthField(after="show_from")

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
        today = datetime.now().replace(year=DayMonthField.get_base_year())
        nextYear = today.replace(year=today.year + 1)

        try:
            image = cls.objects.filter(
                Q(show_from__lte=today, show_to__gte=today) | Q(show_from__lte=nextYear, show_to__gte=nextYear)
            ).order_by("show_from")[0]
        except IndexError:
            image = None

        return image
