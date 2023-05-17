# Django
from django import template

# Locals
from ..models import EFFECTS, Logo

register = template.Library()


@register.inclusion_tag("tags/effects.html")
def effects():
    logo = Logo.get_current_logo() or Logo()
    return {k: getattr(logo, k) for k in EFFECTS}


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
