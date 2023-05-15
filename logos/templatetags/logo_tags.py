# Django
from django import template
from django.utils.safestring import mark_safe

# Locals
from ..models import Logo

register = template.Library()


@register.inclusion_tag("tags/effects.html")
def effects():
    if logo := Logo.get_current_logo():
        return {
            "fireworks": logo.fireworks,
            "snow": logo.snow,
            "confetti": logo.confetti,
        }
    else:
        return {
            "fireworks": False,
            "snow": False,
        }


@register.simple_tag()
def effects_container():
    if logo := Logo.get_current_logo():
        if logo.fireworks:
            return mark_safe('<div class="fireworks"></div>')

    return ""


@register.inclusion_tag("tags/logo.html")
def logo():
    if logo := Logo.get_current_logo():
        return {
            "logo": logo.svg,
            "title": logo.title or None,
        }
    else:
        return {
            "logo": None,
            "title": None,
        }
