from django import template

from banners.models import Banner

register = template.Library()


@register.simple_tag(takes_context=True)
def get_banner(context):
    try:
        if banner_image := context.get("page", None).banner_image:
            return banner_image
    except AttributeError:
        pass

    banner = Banner.get_current_image()
    return banner.image if banner else None
