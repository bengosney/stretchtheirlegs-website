# Django
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

# Third Party
from django_extensions.db import fields

# Wagtail
from wagtail.admin.panels import FieldPanel, MultiFieldPanel

# First Party
from fh_utils.models import StatusDateRangeMixin


class Message(StatusDateRangeMixin, models.Model):
    title = models.CharField(_("Title"), max_length=150)
    message = models.TextField(_("Message"), max_length=1280)
    dismissible = models.BooleanField(_("Dismissible"), default=True)

    slug = fields.AutoSlugField(populate_from="title")

    class Meta:
        default_manager_name = "admin_objects"

    def __str__(self):
        return f"{self.title}"

    def dismiss(self, session):
        if not self.dismissible:
            return

        session[self.session_key] = True
        session.modified = True

    @property
    def dismiss_url(self):
        return reverse("site_messages:dismiss", kwargs={"slug": self.slug})

    @property
    def session_key(self):
        return f"message-{self.slug}-dismissed"

    @classmethod
    def get_messages(cls, session):
        return [o for o in cls.objects.all() if not session.get(o.session_key, False) or not o.dismissible]

    panels = StatusDateRangeMixin.mixin_panels + [
        MultiFieldPanel(
            [
                FieldPanel("title"),
                FieldPanel("message"),
                FieldPanel("dismissible"),
            ],
            heading="Message",
        ),
    ]
