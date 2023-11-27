# Wagtail
from wagtail.contrib.modeladmin.mixins import ThumbnailMixin
from wagtail.snippets.models import register_snippet
from wagtail.snippets.views.snippets import SnippetViewSet

# Locals
from .models import Banner


class BannerAdmin(ThumbnailMixin, SnippetViewSet):
    model = Banner
    menu_label = "Banner Images"
    icon = "image"
    list_display = (
        "image",
        "admin_preview",
        "status_name",
        "admin_show_from",
        "admin_show_to",
    )
    list_filter = ("status",)
    add_to_admin_menu = True


register_snippet(BannerAdmin)
