# Django
from django.db import models

# Wagtail
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.contrib.forms.models import AbstractEmailForm
from wagtail.core import blocks
from wagtail.core.fields import RichTextField, StreamField
from wagtail.core.models import Page
from wagtail.images.edit_handlers import ImageChooserPanel

# Locals
from .blocks import ServicesBlock


class HomePage(Page):
    show_in_menus_default = True

    body = StreamField(
        [
            ("Paragraph", blocks.RichTextBlock()),
            ("Services", ServicesBlock()),
        ]
    )

    parent_page_types = ["wagtailcore.Page"]

    content_panels = Page.content_panels + [
        StreamFieldPanel("body"),
    ]


class InfoPage(Page):
    show_in_menus_default = True


class ServicePage(Page):
    show_in_menus_default = True

    short_description = models.CharField(max_length=350, blank=True)
    body = RichTextField(blank=True)
    image = models.ForeignKey("wagtailimages.Image", null=True, blank=True, on_delete=models.SET_NULL, related_name="+")

    content_panels = Page.content_panels + [ImageChooserPanel("image"), FieldPanel("short_description"), FieldPanel("body")]


class FormPage(AbstractEmailForm):
    show_in_menus_default = True


class MenuPage(Page):
    show_in_menus_default = True
