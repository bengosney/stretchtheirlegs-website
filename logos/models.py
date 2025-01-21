from typing import ClassVar

from django import forms
from django.contrib import admin
from django.db import models
from django.db.models import Q
from django.utils.html import mark_safe
from django.utils.translation import gettext_lazy as _

from wagtail.admin.panels import FieldPanel, FieldRowPanel, MultiFieldPanel, Panel

from fh_utils.managers import DatePeriodManager, StatusManager
from fh_utils.models import StatusDatePeriodMixin, StatusMixin
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


class EasterManager(StatusManager):
    def get_queryset(self):
        if is_easter():
            return super().get_queryset().filter(Q(easter=True) | Q(DatePeriodManager._get_q()))
        else:
            return super().get_queryset().filter(Q(easter=False) & Q(DatePeriodManager._get_q()))


class Logo(StatusDatePeriodMixin, models.Model):
    title = models.TextField(_("Title"))
    logo = models.FileField(_("Logo SVG"), upload_to="logos")
    easter = models.BooleanField(_("Easter"), db_default=False)

    effect = models.CharField(
        _("Effect"),
        max_length=max([len(e) for e in EFFECTS]),
        choices=list(zip(EFFECTS, [e.capitalize() for e in EFFECTS])),
        default="",
        blank=True,
    )

    objects = EasterManager()

    panels: ClassVar[list[Panel]] = [
        *StatusMixin.mixin_panels,
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
        ordering: ClassVar[list[str]] = ["-easter", "show_from"]

    def __getattr__(self, attr):
        if attr in EFFECTS:
            return attr == self.effect

        raise AttributeError(self, attr)

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
