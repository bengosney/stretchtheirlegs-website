from django.test import TestCase

from fh_utils import ModelStatus
from fh_utils.models import StatusMixin
from fh_utils.tests.abstract_mixin import AbstractModelMixinTestCase


class StatusTests(AbstractModelMixinTestCase, TestCase):
    mixin = StatusMixin

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

    def test_status_string(self):
        obj = self.model.objects.create(status=ModelStatus.DRAFT_STATUS)
        self.assertEqual(f"{obj}", f"{ModelStatus.DRAFT_STATUS}")
