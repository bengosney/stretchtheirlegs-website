# Django
from django import template

# Locals
from ..models import Banner

register = template.Library()


@register.simple_tag(takes_context=True)
def get_banner(context):
    try:
        banner = Banner.objects.all()[0]
        return banner.image
    except IndexError:
        return None
