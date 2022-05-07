# Django
from django.db import models

# Wagtail
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.contrib.forms.models import AbstractEmailForm
from wagtail.contrib.settings.models import BaseSetting, register_setting
from wagtail.core import blocks
from wagtail.core.fields import RichTextField, StreamField
from wagtail.core.models import Page
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.snippets.models import register_snippet

# Locals
from .blocks import ItemBlock, ServicesBlock


@register_setting
class SiteSettings(BaseSetting):
    phone_number = models.CharField(max_length=255, help_text="Phone number to show in the footer", default="")
    facebook = models.URLField(help_text="Your Facebook page URL", default="")
    email = models.EmailField(max_length=150, help_text="Email address to show in the footer", default="")


@register_snippet
class Membership(models.Model):
    name = models.CharField(max_length=255)
    url = models.URLField(blank=True)
    image = models.ForeignKey("wagtailimages.Image", null=True, blank=True, on_delete=models.SET_NULL, related_name="+")

    panels = [
        FieldPanel("name"),
        FieldPanel("url"),
        ImageChooserPanel("image"),
    ]

    def __str__(self):
        return self.name


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

    body = StreamField(
        [
            ("Paragraph", blocks.RichTextBlock()),
            ("Services", ServicesBlock()),
            ("Item", ItemBlock()),
        ]
    )

    content_panels = Page.content_panels + [
        StreamFieldPanel("body"),
    ]


class ServicePage(Page):
    show_in_menus_default = True

    short_description = models.CharField(max_length=350, blank=True)
    body = RichTextField(blank=True)
    image = models.ForeignKey("wagtailimages.Image", null=True, blank=True, on_delete=models.SET_NULL, related_name="+")

    content_panels = Page.content_panels + [
        ImageChooserPanel("image"),
        FieldPanel("short_description"),
        FieldPanel("body"),
    ]


class FormPage(AbstractEmailForm):
    show_in_menus_default = True


class MenuPage(Page):
    show_in_menus_default = True
