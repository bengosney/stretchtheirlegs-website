# Django
from django import template

# Locals
from ..models import Banner

register = template.Library()


@register.simple_tag(takes_context=True)
def get_banner(context):
    banner = Banner.objects.all()[0]

    return banner.image
