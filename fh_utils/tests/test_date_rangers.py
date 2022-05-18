# Third Party
from hypothesis import given
from hypothesis.extra.django import TestCase
from hypothesis.strategies import dates

# First Party
from fh_utils import ModelStatus
from fh_utils.models import statusDateRangeMixin

# Locals
from . import today, tomorrow, yesterday
from .abstract_mixin import AbstractModelMixinTestCase


class DateRangeTests(AbstractModelMixinTestCase, TestCase):
    mixin = statusDateRangeMixin

    @given(published_from=dates(max_value=today), published_to=dates(min_value=today))
    def test_get(self, published_from, published_to) -> None:
        self.model.objects.create(published_from=published_from, published_to=published_to, status=ModelStatus.LIVE_STATUS)
        all_items = self.model.objects.all()
        self.assertEqual(len(all_items), 1)

    @given(published_from=dates(max_value=yesterday), published_to=dates(max_value=yesterday))
    def test_date_in_past(self, published_from, published_to) -> None:
        self.model.objects.create(published_from=published_from, published_to=published_to, status=ModelStatus.LIVE_STATUS)
        all_items = self.model.objects.all()
        self.assertEqual(len(all_items), 0)

    @given(published_from=dates(min_value=tomorrow), published_to=dates(min_value=tomorrow))
    def test_date_in_future(self, published_from, published_to) -> None:
        self.model.objects.create(published_from=published_from, published_to=published_to, status=ModelStatus.LIVE_STATUS)
        all_items = self.model.objects.all()
        self.assertEqual(len(all_items), 0)
