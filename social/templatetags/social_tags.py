import contextlib
import json
from collections.abc import Iterable

from django import template
from django.utils.safestring import mark_safe
from wagtail.models import Site

from banners.models import Banner
from social.models import Social

register = template.Library()


@register.filter()
def jsonld(value, indent=None):
    json_output = json.dumps(value, indent=indent)
    return mark_safe(f"""<script type="application/ld+json">{json_output}</script>""")


def get_breadcrumbs(ancestors: list) -> Iterable:
    for i, ancestor_page in enumerate(ancestors, start=1):
        ancestor = ancestor_page.get_specific()
        if ancestor.id > 1:
            yield {
                "@type": "ListItem",
                "position": i,
                "item": {
                    "@id": ancestor.get_full_url() or ancestor.title,
                    "name": ancestor.title,
                },
            }


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

    flat_context = context.flatten()

    with contextlib.suppress(KeyError):
        jsonld.append(
            {
                "@context": "https://schema.org",
                "@type": "BreadcrumbList",
                "itemListElement": list(get_breadcrumbs(flat_context["page"].get_ancestors(inclusive=True))),
            }
        )

    with contextlib.suppress(KeyError, AttributeError):
        jsonld.append(flat_context["page"].get_jsonld())

    return {
        "og_description": settings.description,
        "og_image": settings.image,
        "og_title": site.site_name,
        "og_url": site.root_url,
        "jsonld": jsonld,
    }
