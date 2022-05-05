# Wagtail
from wagtail.contrib.forms.models import AbstractEmailForm
from wagtail.core.models import Page


class HomePage(Page):
    show_in_menus_default = True


class InfoPage(Page):
    show_in_menus_default = True


class ServicePage(Page):
    show_in_menus_default = True


class FormPage(AbstractEmailForm):
    show_in_menus_default = True


class MenuPage(Page):
    show_in_menus_default = True
