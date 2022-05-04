# Wagtail
from wagtail.core.models import Page
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField


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
    