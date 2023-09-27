# Wagtail
from wagtail.snippets.models import register_snippet
from wagtail.snippets.views.snippets import SnippetViewSet

# Locals
from .models import Banner


class BannerAdmin(SnippetViewSet):
    model = Banner
    menu_label = "Banner Images"
    menu_icon = "image"
    list_display = ("image", "status", "show_from", "show_to")
    list_filter = ("status",)


register_snippet(BannerAdmin)
