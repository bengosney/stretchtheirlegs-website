# Django
from django.test import TestCase

# Third Party
from model_bakery import baker

# Locals
from .models import Message


class TestSiteMessages(TestCase):
    def test_key(self):
        msg = baker.make(Message)
        self.assertEqual(msg.session_key, f"message-{msg.slug}-dismissed")
