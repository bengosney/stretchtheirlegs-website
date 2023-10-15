# Wagtail
from wagtail.snippets.models import register_snippet
from wagtail.snippets.views.snippets import SnippetViewSet

# Locals
from .models import Logo


class LogoAdmin(SnippetViewSet):
    model = Logo
    menu_label = "Logos"
    icon = "image"
    list_display = ("title", "status", "show_from", "show_to", "logo")
    list_filter = ("status",)
    search_fields = ("title",)
    add_to_admin_menu = True


register_snippet(LogoAdmin)
