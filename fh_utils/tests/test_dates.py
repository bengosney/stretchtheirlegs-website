from hypothesis import given
from hypothesis.extra.django import TestCase
from hypothesis.strategies import dates

from fh_utils import ModelStatus
from fh_utils.models import StatusDateMixin
from fh_utils.tests import tomorrow, yesterday
from fh_utils.tests.abstract_mixin import AbstractModelMixinTestCase


class DateTests(AbstractModelMixinTestCase, TestCase):
    mixin = StatusDateMixin

    @given(published=dates(max_value=yesterday))
    def test_get(self, published):
        self.model.objects.create(published=published, status=ModelStatus.LIVE_STATUS)
        all_items = self.model.objects.all()
        self.assertEqual(len(all_items), 1)

    @given(published=dates(min_value=tomorrow))
    def test_not_yet(self, published):
        self.model.objects.create(published=published, status=ModelStatus.LIVE_STATUS)
        all_items = self.model.objects.all()
        self.assertEqual(len(all_items), 0)
