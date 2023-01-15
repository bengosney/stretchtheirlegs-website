# Standard Library
import contextlib

# Django
from django.db import models
from django.http import Http404

# Wagtail
from wagtail.admin.edit_handlers import FieldPanel, FieldRowPanel, InlinePanel, MultiFieldPanel
from wagtail.contrib.forms.edit_handlers import FormSubmissionsPanel
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField
from wagtail.contrib.settings.models import BaseSetting, register_setting
from wagtail.core import blocks
from wagtail.core.fields import RichTextField, StreamField
from wagtail.core.models import Page
from wagtail.snippets.models import register_snippet

# Third Party
from modelcluster.fields import ParentalKey

# Locals
from .blocks import FormBlock, ImageRow, ItemBlock, ServicesBlock
from .utils import send_mail


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

    parent_page_types = ["wagtailcore.Page"]

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("banner_title"),
                FieldPanel("banner_sub_title"),
            ],
            "Banner",
        ),
        FieldPanel("body"),
    ]


class InfoPage(Page, ParentTools):
    show_in_menus_default = True

    body = StreamField(
        [
            ("Paragraph", blocks.RichTextBlock()),
            ("Services", ServicesBlock()),
            ("Item", ItemBlock()),
            ("ImageRow", ImageRow()),
        ],
        use_json_field=True,
    )

    content_panels = Page.content_panels + [
        FieldPanel("body"),
    ]


class ServicePage(Page, ParentTools):
    show_in_menus_default = True

    sub_title = models.CharField(max_length=120, blank=True, default="Details")
    short_description = models.CharField(max_length=350, blank=True)
    body = RichTextField(blank=True)
    image = models.ForeignKey("wagtailimages.Image", null=True, blank=True, on_delete=models.SET_NULL, related_name="+")

    content_panels = Page.content_panels + [
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


class FormPage(AbstractEmailForm, ParentTools):
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

    content_panels = AbstractEmailForm.content_panels + [
        FormSubmissionsPanel(),
        FieldPanel("body"),
        InlinePanel("form_fields", label="Form fields"),
        MultiFieldPanel(
            [
                FieldPanel("submit_text"),
                FieldPanel("thank_you_text"),
            ],
            "Submit",
        ),
        MultiFieldPanel(
            [
                FieldRowPanel(
                    [
                        FieldPanel("from_address", classname="col6"),
                        FieldPanel("to_address", classname="col6"),
                    ]
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


class MenuPage(Page):
    show_in_menus_default = True

    def get_url_parts(self, request=None):
        return None

    def get_sitemap_urls(self, request=None):
        return []

    def serve(self, request, *args, **kwargs):
        raise Http404()
