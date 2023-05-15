# Django
from django.db import models
from django.utils.translation import gettext_lazy as _

# Wagtail
from wagtail.admin.panels import FieldPanel, MultiFieldPanel

# First Party
from fh_utils.models import statusDatePeriodMixin, statusMixin

EFFECT_SNOW = "snow"
EFFECT_FIREWORKS = "fireworks"

EFFECTS = (
    EFFECT_SNOW,
    EFFECT_FIREWORKS,
)


class Logo(statusDatePeriodMixin, models.Model):
    title = models.TextField(_("Title"))
    logo = models.FileField(_("Logo SVG"), upload_to="logos")

    effect = models.CharField(
        _("Effect"),
        max_length=max([len(e) for e in EFFECTS]),
        choices=zip(EFFECTS, [e.capitalize() for e in EFFECTS]),
        default=None,
        blank=True,
        null=True,
    )

    panels = [
        *statusMixin.mixin_panels,
        MultiFieldPanel(
            [
                FieldPanel("show_from"),
                FieldPanel("show_to"),
            ],
            heading="Date Range",
        ),
        MultiFieldPanel(
            [
                FieldPanel("title"),
                FieldPanel("logo"),
                FieldPanel("effect"),
            ],
            heading="Details",
        ),
    ]

    class Meta:
        default_manager_name = "admin_objects"

    def __str__(self):
        return self.title

    @property
    def svg(self) -> str:
        try:
            return self.logo.read().decode("utf-8")
        except FileNotFoundError:
            return ""

    @classmethod
    def get_current_logo(cls):
        try:
            return cls.objects.all().order_by("show_from")[0]
        except IndexError:
            return None

    def __getattr__(self, attr):
        if attr in EFFECTS:
            return attr == self.effect

        raise AttributeError(f"{self.__class__} does not contain {attr}")
