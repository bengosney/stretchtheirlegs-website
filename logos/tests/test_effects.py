from datetime import date

from freezegun import freeze_time

from django.test import TestCase

from logos.models import EFFECT_SNOW, EFFECTS, Logo
from logos.templatetags.logo_tags import effects


class LogoEffectsTests(TestCase):
    def make_logo(self, **kwargs) -> Logo:
        defaults = {
            "show_from": date(2020, 1, 1),
            "show_to": date(2020, 2, 1),
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

    def test_effect(self):
        logo = self.make_logo(effect=EFFECT_SNOW)
        logo.save()

        with freeze_time("2020-01-02"):
            context = effects()

        self.assertEqual(sum(int(e) for e in context.values()), 1)
        self.assertTrue(context["snow"])
        self.assertListEqual(sorted(list(context.keys())), sorted(list(EFFECTS)))

    def test_no_current_logo(self):
        logo = self.make_logo(effect=EFFECT_SNOW)
        logo.save()

        with freeze_time("2020-12-12"):
            self.assertIsNone(Logo.get_current_logo())

    def test_effect_no_logo(self):
        logo = self.make_logo(effect=EFFECT_SNOW)
        logo.save()

        with freeze_time("2020-12-12"):
            context = effects()

        self.assertDictEqual(context, {k: False for k in EFFECTS})
