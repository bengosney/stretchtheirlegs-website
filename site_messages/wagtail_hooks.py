# Wagtail
from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register

# Locals
from .models import Message


class MessageAdmin(ModelAdmin):
    model = Message
    menu_label = "Site Messages"
    menu_icon = "list-ul"
    list_display = ("title", "dismissible", "status", "published_from", "published_to")
    list_filter = ("status",)


modeladmin_register(MessageAdmin)
