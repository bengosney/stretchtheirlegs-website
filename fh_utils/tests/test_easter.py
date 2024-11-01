from datetime import date

from freezegun import freeze_time

from django.test import TestCase

from fh_utils.utils import is_easter, next_easter


class NextEasterTests(TestCase):
    def test_jan(self):
        with freeze_time("2020-01-01"):
            self.assertEqual(next_easter(), date(2020, 4, 12))

    def test_dec(self):
        with freeze_time("2020-12-01"):
            self.assertEqual(next_easter(), date(2021, 4, 4))


class IsEasterTests(TestCase):
    def test_easter(self):
        with freeze_time("2020-04-12"):
            self.assertTrue(is_easter())

    def test_not_easter(self):
        with freeze_time("2020-04-13"):
            self.assertFalse(is_easter())
