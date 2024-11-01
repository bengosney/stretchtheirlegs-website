from django.db import models

from wagtail.contrib.settings.models import BaseSiteSetting, register_setting


@register_setting
class Robots(BaseSiteSetting):
    contents = models.TextField(blank=True)
