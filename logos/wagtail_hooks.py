from django.utils.html import format_html

from wagtail import hooks
from wagtail.snippets.models import register_snippet
from wagtail.snippets.views.snippets import SnippetViewSet

from logos.models import Logo


class LogoAdmin(SnippetViewSet):
    model = Logo
    menu_label = "Logos"
    icon = "image"
    list_display = ("title", "admin_preview", "status_name", "admin_show_from", "admin_show_to")
    list_filter = ("status",)
    search_fields = ("title",)
    add_to_admin_menu = True


register_snippet(LogoAdmin)


@hooks.register("insert_editor_js")
def load_alpinejs():
    return format_html('<script defer src="https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js"></script>')
