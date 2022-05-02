# Django
from django.db import models

# Wagtail
from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel

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
