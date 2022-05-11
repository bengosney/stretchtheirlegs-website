# Standard Library
from datetime import date

# Django
from django.test import TestCase

# Third Party
from freezegun import freeze_time
from icecream import ic

# Locals
from .models import Banner


class DayMonthFieldTests(TestCase):
    def test_pre_save(self):
        with freeze_time("2020-01-01"):
            banner = Banner.objects.create(show_from=date(2020, 1, 1))
            self.assertEqual(banner.show_from, date(1970, 1, 1))


class BannerTests(TestCase):
    def test_get(self):
        created = Banner.objects.create(show_from=date(2020, 1, 1), show_to=date(2020, 12, 31))

        banner = Banner.getCurrentImage()

        self.assertEqual(created, banner)

    def test_image_dates(self):
        Banner.objects.create(show_from=date(2020, 1, 1), show_to=date(2020, 6, 1))
        created_second = Banner.objects.create(show_from=date(2020, 6, 2), show_to=date(2020, 12, 31))

        for b in Banner.objects.all():
            ic(b.show_from, b.show_to)

        with freeze_time("2022-07-01"):
            banner = Banner.getCurrentImage()

            self.assertEqual(created_second, banner)
