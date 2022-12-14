# Django
from django import template

# Locals
from ..models import Logo

register = template.Library()


@register.inclusion_tag("tags/fireworks.html")
def fireworks():
    if logo := Logo.get_current_logo():
        print(f"logo.fireworks: {logo.fireworks}")
        return {"fireworks": logo.fireworks}
    else:
        return {"fireworks": False}


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
