# Django
from django import template

# Locals
from ..models import Logo

register = template.Library()


@register.inclusion_tag("tags/effects.html")
def effects():
    if logo := Logo.get_current_logo():
        return {
            "fireworks": logo.fireworks,
            "snow": logo.snow,
        }
    else:
        return {
            "fireworks": False,
            "snow": False,
        }


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
