# Standard Library
import json

# Django
from django import template
from django.utils.safestring import mark_safe

# Wagtail
from wagtail.models import Site

# First Party
from banners.models import Banner

# Locals
from ..models import Social

register = template.Library()


@register.filter()
def jsonld(value, indent=None):
    return mark_safe(
        f"""
<script type="application/ld+json">{json.dumps(value, indent=indent)}</script>
    """
    )


@register.inclusion_tag("tags/social_tags.html", takes_context=True)
def social_tags(context):
    site = Site.find_for_request(context["request"])
    settings = Social.for_request(context["request"])

    context["site"] = site

    if banner := Banner.get_current_image():
        context["banner"] = banner.image.get_rendition("fill-1920x1080|jpegquality-70").url

    try:
        jsonld_template = template.Template(settings.json_ld)
        jsonld = json.loads(jsonld_template.render(context))
        if not isinstance(jsonld, list):
            jsonld = [jsonld]
    except Exception:
        jsonld = []

    try:
        context.flatten()["page"]
    except KeyError:
        pass

    return {
        "og_description": settings.description,
        "og_image": settings.image,
        "og_title": site.site_name,
        "og_url": site.root_url,
        "jsonld": jsonld,
    }
