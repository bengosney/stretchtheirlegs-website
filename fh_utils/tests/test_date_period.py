from datetime import date

from django.test import TestCase
from freezegun import freeze_time

from fh_utils.fields import DayMonthField
from fh_utils.models import StatusDatePeriodMixin
from fh_utils.tests.abstract_mixin import AbstractModelMixinTestCase


class Tests(AbstractModelMixinTestCase, TestCase):
    mixin = StatusDatePeriodMixin

    def test_pre_save(self):
        with freeze_time("2020-01-01"):
            obj = self.model.objects.create(show_from=date(2020, 1, 1), show_to=date(2021, 5, 5))
            obj.save()

            self.assertEqual(obj.show_from, date(DayMonthField.get_base_year(), 1, 1))

    def test_get(self):
        created = self.model.objects.create(show_from=date(2020, 1, 1), show_to=date(2020, 12, 31))

        obj = self.model.objects.all()[0]

        self.assertEqual(created, obj)

    def test_image_dates(self):
        self.model.objects.create(show_from=date(2020, 1, 1), show_to=date(2020, 6, 1)).save()
        created_second = self.model.objects.create(show_from=date(2020, 6, 2), show_to=date(2020, 12, 31))
        created_second.save()

        with freeze_time("2022-07-01"):
            obj = self.model.objects.all()[0]

            self.assertEqual(created_second, obj)

    def test_span_year_end(self):
        self._test_year_span("2021-12-01")

    def test_span_year_start(self):
        self._test_year_span("2021-2-01")

    def _test_year_span(self, arg0):
        self.model.objects.create(show_from=date(2020, 11, 1), show_to=date(2021, 3, 1))
        with freeze_time(arg0):
            obj = self.model.objects.all()[0]

        self.assertIsNotNone(obj)
