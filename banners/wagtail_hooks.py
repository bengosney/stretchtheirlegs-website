# Wagtail
from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register

# Locals
from .models import Banner


class BannerAdmin(ModelAdmin):
    model = Banner
    menu_label = "Banner Images"
    menu_icon = "image"
    list_display = ("status", "show_from", "show_to", "image")
    list_filter = ("status",)


modeladmin_register(BannerAdmin)
