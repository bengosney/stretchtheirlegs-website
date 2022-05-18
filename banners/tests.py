# Standard Library
from datetime import date

# Django
from django.test import TestCase

# Third Party
from freezegun import freeze_time

# Locals
from .fields import DayMonthField
from .models import Banner


class DayMonthFieldTests(TestCase):
    def test_pre_save(self):
        with freeze_time("2020-01-01"):
            banner = Banner.objects.create(show_from=date(2020, 1, 1), show_to=date(2021, 5, 5))
            banner.save()

            self.assertEqual(banner.show_from, date(DayMonthField.get_base_year(), 1, 1))


class BannerTests(TestCase):
    def test_get(self):
        created = Banner.objects.create(show_from=date(2020, 1, 1), show_to=date(2020, 12, 31))

        banner = Banner.getCurrentImage()

        self.assertEqual(created, banner)

    def test_image_dates(self):
        Banner.objects.create(show_from=date(2020, 1, 1), show_to=date(2020, 6, 1)).save()
        created_second = Banner.objects.create(show_from=date(2020, 6, 2), show_to=date(2020, 12, 31))
        created_second.save()

        with freeze_time("2022-07-01"):
            banner = Banner.getCurrentImage()

            self.assertEqual(created_second, banner)

    def test_span_year_end(self):
        self._test_year_span("2021-12-01")

    def test_span_year_start(self):
        self._test_year_span("2021-2-01")

    def _test_year_span(self, arg0):
        Banner.objects.create(show_from=date(2020, 11, 1), show_to=date(2021, 3, 1))
        with freeze_time(arg0):
            banner = Banner.getCurrentImage()

        self.assertIsNotNone(banner)
