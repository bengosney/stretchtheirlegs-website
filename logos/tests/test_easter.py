# Standard Library
from datetime import date

# Django
from django.test import TestCase

# Third Party
from freezegun import freeze_time

# First Party
from logos.models import Logo


class EasterLogoTests(TestCase):
    def make_logo(self, **kwargs) -> Logo:
        defaults = {
            "show_from": date(2020, 1, 1),
            "show_to": date(2020, 2, 1),
            "title": "title",
            "effect": None,
            "easter": False,
        }

        return Logo(**defaults | kwargs)

    def test_make_logo(self):
        logo = self.make_logo(easter=True)

        self.assertEqual(logo.easter, True)
        self.assertEqual(logo.title, "title")

    def test_select_easter(self):
        logo = self.make_logo(easter=True)
        logo.save()

        with freeze_time("2021-04-04"):
            self.assertEqual(logo, Logo.get_current_logo())

    def test_select_easter_first(self):
        self.make_logo(show_from=date(2020, 3, 1), show_to=date(2020, 5, 1)).save()
        logo = self.make_logo(easter=True)
        logo.save()
        self.make_logo(show_from=date(2020, 3, 1), show_to=date(2020, 5, 1)).save()

        with freeze_time("2021-04-04"):
            self.assertEqual(logo, Logo.get_current_logo())

    def test_dont_select_easter(self):
        logo = self.make_logo(easter=True)
        logo.save()

        with freeze_time("2021-05-04"):
            self.assertEqual(None, Logo.get_current_logo())
