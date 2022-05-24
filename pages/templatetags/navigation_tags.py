# Django
from django import template

# Wagtail
from wagtail.core.models import Site

# Locals
from ..models import SiteSettings

register = template.Library()


@register.simple_tag(takes_context=True)
def get_site_root(context):
    return Site.find_for_request(context["request"]).root_page


def has_menu_children(page):
    return page.get_children().live().in_menu().exists()


def has_children(page):
    return page.get_children().live().exists()


def is_active(page, current_page):
    return current_page.url_path.startswith(page.url_path) if current_page else False


@register.inclusion_tag("tags/menu.html", takes_context=True)
def menu(context, parent=None, calling_page=None, level=0):
    level += 1
    parent = parent or get_site_root(context)
    menuitems = list(parent.get_children().live().in_menu())

    for menuitem in menuitems:
        menuitem.show_dropdown = has_menu_children(menuitem)
        menuitem.active = calling_page.url_path.startswith(menuitem.url_path) if calling_page else False
        menuitem.type = "page"

    if level == 1:
        menuitems.insert(0, parent)
        menuitems[0].show_dropdown = False
        menuitems[0].active = calling_page.url_path == menuitems[0].url_path if calling_page else False

    siteSettings = SiteSettings.for_request(context["request"])

    return {
        "level": level,
        "calling_page": calling_page,
        "menuitems": menuitems,
        "request": context["request"],
        "site_settings": siteSettings,
    }


# Retrieves the children of the top menu items for the drop downs
@register.inclusion_tag("tags/top_menu_children.html", takes_context=True)
def top_menu_children(context, parent, calling_page=None):
    menuitems_children = parent.get_children()
    menuitems_children = menuitems_children.live().in_menu()
    for menuitem in menuitems_children:
        menuitem.show_dropdown = has_menu_children(menuitem)
        # We don't directly check if calling_page is None since the template
        # engine can pass an empty string to calling_page
        # if the variable passed as calling_page does not exist.
        menuitem.active = calling_page.url_path.startswith(menuitem.url_path) if calling_page else False
        menuitem.children = menuitem.get_children().live().in_menu()
    return {
        "parent": parent,
        "calling_page": calling_page,
        "menuitems_children": menuitems_children,
        # required by the pageurl tag that we want to use within this template
        "request": context["request"],
    }
