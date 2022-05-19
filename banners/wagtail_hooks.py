# Wagtail
from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register

# First Party
from fh_utils.admin import adminManagerAdmin

# Locals
from .models import Banner


class BannerAdmin(adminManagerAdmin, ModelAdmin):
    model = Banner
    menu_label = "Banner Images"
    menu_icon = "image"
    list_display = ("status", "show_from", "show_to", "image")
    list_filter = ("status",)


modeladmin_register(BannerAdmin)
