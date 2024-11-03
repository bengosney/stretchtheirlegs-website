import contextlib
from textwrap import shorten
from typing import ClassVar

from modelcluster.fields import ParentalKey

from django.conf import settings
from django.db import models
from django.http import Http404

from wagtail import blocks
from wagtail.admin.mail import send_mail
from wagtail.admin.panels import FieldPanel, FieldRowPanel, InlinePanel, MultiFieldPanel, Panel
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField
from wagtail.contrib.forms.panels import FormSubmissionsPanel
from wagtail.contrib.settings.models import BaseSiteSetting, register_setting
from wagtail.fields import RichTextField, StreamField
from wagtail.models import Page
from wagtail.snippets.models import register_snippet

from pages.blocks import FormBlock, ImageRow, ItemBlock, ServicesBlock


@register_setting
class SiteSettings(BaseSiteSetting):
    phone_number = models.CharField(max_length=255, help_text="Phone number to show in the footer", default="")
    facebook = models.URLField(help_text="Your Facebook page URL", default="")
    email = models.EmailField(max_length=150, help_text="Email address to show in the footer", default="")


@register_snippet
class Membership(models.Model):
    name = models.CharField(max_length=255)
    url = models.URLField(blank=True)
    image = models.ForeignKey("wagtailimages.Image", null=True, blank=True, on_delete=models.SET_NULL, related_name="+")

    panels: ClassVar[list[Panel]] = [
        FieldPanel("name"),
        FieldPanel("url"),
        FieldPanel("image"),
    ]

    def __str__(self):
        return self.name


class ParentTools:
    @property
    def parent_title(self):
        with contextlib.suppress(AttributeError):
            parent = self.get_parent().get_specific()
            if not parent.is_site_root():
                return parent.title


class HomePage(Page):
    show_in_menus_default = True

    banner_title = models.CharField(max_length=60)
    banner_sub_title = models.CharField(max_length=120)

    body = StreamField(
        [
            ("Paragraph", blocks.RichTextBlock()),
            ("Services", ServicesBlock()),
            ("ImageRow", ImageRow()),
        ],
        use_json_field=True,
    )

    parent_page_types: ClassVar[list[str]] = ["wagtailcore.Page"]

    content_panels: ClassVar[list[MultiFieldPanel | FieldPanel]] = [
        *Page.content_panels,
        MultiFieldPanel([FieldPanel("banner_title"), FieldPanel("banner_sub_title")], "Banner"),
        FieldPanel("body"),
    ]


class InfoPage(Page, ParentTools):
    show_in_menus_default = True
    sub_heading = models.CharField(max_length=255, default="", blank=True)

    body = StreamField(
        [
            ("Paragraph", blocks.RichTextBlock()),
            ("Services", ServicesBlock()),
            ("Item", ItemBlock()),
            ("ImageRow", ImageRow()),
        ],
        use_json_field=True,
    )

    content_panels: ClassVar[list[Panel]] = [
        *Page.content_panels,
        FieldPanel("sub_heading"),
        FieldPanel("body"),
    ]


class ServicePage(Page, ParentTools):
    show_in_menus_default = True

    sub_heading = models.CharField(max_length=255, default="", blank=True)
    sub_title = models.CharField(max_length=120, blank=True, default="Details")
    short_description = models.CharField(max_length=350, blank=True)
    body = RichTextField(blank=True)
    image = models.ForeignKey("wagtailimages.Image", null=True, blank=True, on_delete=models.SET_NULL, related_name="+")

    content_panels: ClassVar[list[Panel]] = [
        *Page.content_panels,
        FieldPanel("sub_heading"),
        FieldPanel("sub_title"),
        FieldPanel("image"),
        FieldPanel("short_description"),
        FieldPanel("body"),
    ]

    def get_jsonld(self):
        return {
            "@context": "https://schema.org/",
            "@type": "Service",
            "serviceType": self.title,
        }


class FormField(AbstractFormField):
    page = ParentalKey("FormPage", on_delete=models.CASCADE, related_name="form_fields")


def shorten_label(label):
    short = shorten(label, settings.MAX_FORM_TITLE_LENGTH, placeholder="...")
    if short == "...":
        return label[: settings.MAX_FORM_TITLE_LENGTH - 3] + "..."
    return short


class FormPage(AbstractEmailForm, ParentTools):
    sub_heading = models.CharField(max_length=255, default="", blank=True)
    show_in_menus_default = True
    body = StreamField(
        [
            ("Paragraph", blocks.RichTextBlock()),
            ("Form", FormBlock()),
        ],
        blank=True,
        use_json_field=True,
    )
    thank_you_text = RichTextField(blank=True)
    submit_text = models.CharField(max_length=255, default="Submit")

    content_panels: ClassVar[list[Panel]] = [
        *AbstractEmailForm.content_panels,
        FieldPanel("sub_heading"),
        FormSubmissionsPanel(),
        FieldPanel("body"),
        InlinePanel("form_fields", label="Form fields"),
        MultiFieldPanel([FieldPanel("submit_text"), FieldPanel("thank_you_text")], "Submit"),
        MultiFieldPanel(
            [
                FieldRowPanel(
                    [FieldPanel("from_address", classname="col6"), FieldPanel("to_address", classname="col6")]
                ),
                FieldPanel("subject"),
            ],
            "Email",
        ),
    ]

    def send_mail(self, form):
        addresses = [x.strip() for x in self.to_address.split(",")]

        if reply_to := form.cleaned_data.get("email"):
            reply_to = [r.strip() for r in reply_to.split(",")]

        return send_mail(self.subject, self.render_email(form), addresses, self.from_address, reply_to=reply_to)

    def get_data_fields(self):
        return [(name, shorten_label(label)) for name, label in super().get_data_fields()]


class MenuPage(Page):
    show_in_menus_default = True

    def get_url_parts(self, request=None):
        return None

    def get_sitemap_urls(self, request=None):
        return []

    def serve(self, request, *args, **kwargs):
        raise Http404()

    def get_preview_template(self, request, mode_name):
        return "404.html"
