# Django
from django.test import TestCase

# First Party
from fh_utils import ModelStatus
from fh_utils.models import statusMixin

# Locals
from .abstract_mixin import AbstractModelMixinTestCase


class StatusTests(AbstractModelMixinTestCase, TestCase):
    mixin = statusMixin

    def test_live(self):
        self.model.objects.create(status=ModelStatus.LIVE_STATUS)
        all_items = self.model.objects.all()
        self.assertEqual(len(all_items), 1)

    def test_draft(self):
        self.model.objects.create(status=ModelStatus.DRAFT_STATUS)
        all_items = self.model.objects.all()
        self.assertEqual(len(all_items), 0)

    def test_hidden(self):
        self.model.objects.create(status=ModelStatus.HIDDEN_STATUS)
        all_items = self.model.objects.all()
        self.assertEqual(len(all_items), 0)
