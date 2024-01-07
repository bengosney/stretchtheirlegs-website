# Django
from django import forms
from django.contrib import admin
from django.db import models
from django.db.models import Q
from django.utils.html import mark_safe
from django.utils.translation import gettext_lazy as _

# Wagtail
from wagtail.admin.panels import FieldPanel, FieldRowPanel, MultiFieldPanel

# First Party
from fh_utils.managers import datePeriodManager, statusManager
from fh_utils.models import statusDatePeriodMixin, statusMixin
from fh_utils.utils import is_easter

EFFECT_SNOW = "snow"
EFFECT_FIREWORKS = "fireworks"
EFFECT_CONFETTI = "confetti"
EFFECT_EXPLOSIONS = "explosions"

EFFECTS = (
    EFFECT_SNOW,
    EFFECT_FIREWORKS,
    EFFECT_CONFETTI,
    EFFECT_EXPLOSIONS,
)


class EasterManager(statusManager):
    def get_queryset(self):
        return super().get_queryset().filter(Q(easter=is_easter()) | Q(datePeriodManager._get_q()))


class Logo(statusDatePeriodMixin, models.Model):
    title = models.TextField(_("Title"))
    logo = models.FileField(_("Logo SVG"), upload_to="logos")
    easter = models.BooleanField(_("Easter"), db_default=False)

    effect = models.CharField(
        _("Effect"),
        max_length=max([len(e) for e in EFFECTS]),
        choices=zip(EFFECTS, [e.capitalize() for e in EFFECTS]),
        default=None,
        blank=True,
        null=True,
    )

    objects = EasterManager()

    panels = [
        *statusMixin.mixin_panels,
        MultiFieldPanel(
            [
                FieldPanel("title"),
                FieldPanel("logo"),
                FieldPanel("effect"),
            ],
            heading="Details",
        ),
        MultiFieldPanel(
            [

                FieldRowPanel(
                    [
                        FieldPanel("show_from"),
                        FieldPanel("show_to"),
                    ],
                    attrs={
                        "x-show": "easter == false",
                        "x-transition": True,
                    },
                ),
                FieldPanel(
                    "easter",
                    widget=forms.CheckboxInput(
                        attrs={
                            "x-model": "easter",
                            "x-init": "easter = $el.checked",
                        }
                    ),
                ),
            ],
            attrs={
                "x-data": "{ easter: false }",
            },
            heading="Date Range",
        ),
    ]

    class Meta:
        default_manager_name = "admin_objects"
        ordering = ["-easter", "show_from"]

    def __str__(self):
        return self.title

    @admin.display(description="preview")
    def admin_preview(self) -> str:
        return mark_safe(self.svg)

    @property
    def svg(self) -> str:
        try:
            return self.logo.read().decode("utf-8")
        except FileNotFoundError:
            return ""

    @classmethod
    def get_current_logo(cls):
        try:
            return cls.objects.all()[0]
        except IndexError:
            return None

    def __getattr__(self, attr):
        if attr in EFFECTS:
            return attr == self.effect

        raise AttributeError(f"{self.__class__} does not contain {attr}")
