from wagtail.snippets.models import register_snippet
from wagtail.snippets.views.snippets import SnippetViewSet

from site_messages.models import Message


class MessageAdmin(SnippetViewSet):
    model = Message
    menu_label = "Site Messages"
    icon = "tasks"
    list_display = ("title", "dismissible", "status", "published_from", "published_to")
    list_filter = ("status",)
    add_to_settings_menu = True


register_snippet(MessageAdmin)
