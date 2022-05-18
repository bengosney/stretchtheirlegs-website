# Third Party
from hypothesis import given
from hypothesis.extra.django import TestCase
from hypothesis.strategies import dates

# First Party
from modulestatus import ModelStatus
from modulestatus.models import statusDateMixin

# Locals
from . import tomorrow, yesterday
from .abstract_mixin import AbstractModelMixinTestCase


class DateTests(AbstractModelMixinTestCase, TestCase):
    mixin = statusDateMixin

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
