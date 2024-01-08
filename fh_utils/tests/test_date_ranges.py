# Standard Library
import datetime

# Django
from django.core.exceptions import ValidationError

# Third Party
from hypothesis import given
from hypothesis.extra.django import TestCase
from hypothesis.strategies import dates

# First Party
from fh_utils import ModelStatus
from fh_utils.models import statusDateRangeMixin

# Locals
from . import today, tomorrow, yesterday
from .abstract_mixin import AbstractModelMixinTestCase, clean_models


class DateRangeTests(AbstractModelMixinTestCase, TestCase):
    mixin = statusDateRangeMixin

    @clean_models
    @given(published_from=dates(max_value=today), published_to=dates(min_value=today))
    def test_get(self, published_from, published_to) -> None:
        self.model.objects.create(published_from=published_from, published_to=published_to, status=ModelStatus.LIVE_STATUS)
        all_items = self.model.objects.all()
        self.assertEqual(len(all_items), 1)

    @clean_models
    @given(published_from=dates(max_value=yesterday + datetime.timedelta(days=-1)))
    def test_date_in_past(self, published_from) -> None:
        published_to = published_from + datetime.timedelta(days=1)
        self.model.objects.create(published_from=published_from, published_to=published_to, status=ModelStatus.LIVE_STATUS)
        all_items = self.model.objects.all()
        self.assertEqual(len(all_items), 0)

    @clean_models
    @given(published_from=dates(min_value=tomorrow))
    def test_date_in_future(self, published_from) -> None:
        published_to = published_from + datetime.timedelta(days=1)
        self.model.objects.create(published_from=published_from, published_to=published_to, status=ModelStatus.LIVE_STATUS)
        all_items = self.model.objects.all()
        self.assertEqual(len(all_items), 0)

    @given(published_from=dates(max_value=yesterday))
    def test_has_passed(self, published_from):
        published_to = published_from + datetime.timedelta(days=1)

        obj = self.model.objects.create(
            published_from=published_from,
            published_to=published_to,
            status=ModelStatus.LIVE_STATUS,
        )
        self.assertTrue(obj.has_passed)

    @given(published_from=dates(min_value=today))
    def test_has_not_passed(self, published_from):
        published_to = published_from + datetime.timedelta(days=1)

        obj = self.model.objects.create(
            published_from=published_from,
            published_to=published_to,
            status=ModelStatus.LIVE_STATUS,
        )
        self.assertFalse(obj.has_passed)

    def test_invalid_date_range(self):
        with self.assertRaises(ValidationError):
            self.model.objects.create(
                published_from=tomorrow,
                published_to=yesterday,
                status=ModelStatus.LIVE_STATUS,
            )

    def test_valid_date_range(self):
        self.model.objects.create(
            published_from=yesterday,
            published_to=tomorrow,
            status=ModelStatus.LIVE_STATUS,
        )
