# Django
from django import template

# Locals
from ..models import Logo

register = template.Library()


@register.inclusion_tag("tags/logo.html")
def logo():
    if logo := Logo.get_current_logo():
        return {
            "logo": logo.svg,
            "title": logo.title or "",
        }
    else:
        return {
            "logo": None,
            "title": "Stretch Their Legs",
        }
