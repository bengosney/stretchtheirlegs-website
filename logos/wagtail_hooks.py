# Wagtail
from wagtail.snippets.models import register_snippet
from wagtail.snippets.views.snippets import SnippetViewSet

# Locals
from .models import Logo


class LogoAdmin(SnippetViewSet):
    model = Logo
    menu_label = "Logos"
    icon = "image"
    list_display = ("title", "admin_preview", "status_name", "admin_show_from", "admin_show_to")
    list_filter = ("status",)
    search_fields = ("title",)
    add_to_admin_menu = True


register_snippet(LogoAdmin)
