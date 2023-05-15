# Standard Library
from datetime import date

# Django
from django.test import TestCase

# First Party
from logos.models import EFFECT_SNOW, Logo


class NavigationTagsTests(TestCase):
    def setUp(self):
        pass

    def make_logo(self, **kwargs) -> Logo:
        defaults = {
            "show_from": date(2020, 1, 1),
            "show_to": date(2021, 1, 1),
            "title": "title",
            "effect": None,
        }

        return Logo(**defaults | kwargs)

    def test_make_logo(self):
        logo = self.make_logo(effect=EFFECT_SNOW)

        self.assertEqual(logo.effect, EFFECT_SNOW)
        self.assertEqual(logo.title, "title")

    def test_attribute(self):
        logo = self.make_logo(effect=EFFECT_SNOW)

        self.assertEqual(logo.effect, EFFECT_SNOW)
        self.assertTrue(logo.snow)
        self.assertFalse(logo.fireworks)

    def test_no_effect(self):
        logo = self.make_logo()

        self.assertIsNone(logo.effect)
        self.assertFalse(logo.snow)
        self.assertFalse(logo.fireworks)

    def test_incorrect_attribute(self):
        logo = self.make_logo()

        with self.assertRaises(AttributeError):
            logo.some_effect_that_doest_exist
