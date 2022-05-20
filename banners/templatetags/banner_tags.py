# Django
from django import template

# Locals
from ..models import Banner

register = template.Library()


@register.simple_tag(takes_context=True)
def get_banner(context):
    return banner.image if (banner := Banner.get_current_image()) else None
