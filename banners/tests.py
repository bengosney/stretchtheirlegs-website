from datetime import date

from freezegun import freeze_time

from django.test import TestCase

from banners.models import Banner
from fh_utils.fields import DayMonthField


class BannerTests(TestCase):
    def test_pre_save(self):
        with freeze_time("2020-01-01"):
            banner = Banner.objects.create(show_from=date(2020, 1, 1), show_to=date(2021, 5, 5))
            banner.save()

            self.assertEqual(banner.show_from, date(DayMonthField.get_base_year(), 1, 1))

    def test_get(self):
        created = Banner.objects.create(show_from=date(2020, 1, 1), show_to=date(2020, 12, 31))

        banner = Banner.get_current_image()

        self.assertEqual(created, banner)

    def test_image_dates(self):
        Banner.objects.create(show_from=date(2020, 1, 1), show_to=date(2020, 6, 1)).save()
        created_second = Banner.objects.create(show_from=date(2020, 6, 2), show_to=date(2020, 12, 31))
        created_second.save()

        with freeze_time("2022-07-01"):
            banner = Banner.get_current_image()

            self.assertEqual(created_second, banner)

    def test_span_year_end(self):
        self._test_year_span("2021-12-01")

    def test_span_year_start(self):
        self._test_year_span("2021-2-01")

    def _test_year_span(self, arg0):
        Banner.objects.create(show_from=date(2020, 11, 1), show_to=date(2021, 3, 1))
        with freeze_time(arg0):
            banner = Banner.get_current_image()

        self.assertIsNotNone(banner)

    def test_no_image(self):
        with freeze_time("2050-01-01"):
            self.assertIsNone(Banner.get_current_image())
