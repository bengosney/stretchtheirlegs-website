# Wagtail
from wagtail.snippets.models import register_snippet
from wagtail.snippets.views.snippets import SnippetViewSet

# Locals
from .models import Message


class MessageAdmin(SnippetViewSet):
    model = Message
    menu_label = "Site Messages"
    menu_icon = "list-ul"
    list_display = ("title", "dismissible", "status", "published_from", "published_to")
    list_filter = ("status",)


register_snippet(MessageAdmin)
