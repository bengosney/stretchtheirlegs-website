from django import template

from pages.models import Membership

register = template.Library()


@register.inclusion_tag("tags/membership_list.html", takes_context=True)
def memberships(context):
    return {
        "memberships": Membership.objects.all(),
        "request": context["request"],
    }
