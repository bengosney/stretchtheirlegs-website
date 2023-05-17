# Wagtail
from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register

# Locals
from .models import Logo


class LogoAdmin(ModelAdmin):
    model = Logo
    menu_label = "Logos"
    menu_icon = "image"
    list_display = ("title", "status", "show_from", "show_to", "logo")
    list_filter = ("status",)
    search_fields = ("title",)


modeladmin_register(LogoAdmin)
