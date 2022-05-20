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

    def test_dissmiss_session(self):
        msg = baker.make(Message)

        session = self.client.session

        self.assertIsNone(session.get(msg.session_key))
        msg.dismiss(session)
        self.assertTrue(session.get(msg.session_key))

    def check_dismissed(self, msg, before, after):
        session = self.client.session
        self.assertEqual(len(Message.get_messages(session)), before)
        msg.dismiss(session)
        self.assertEqual(len(Message.get_messages(session)), after)

    def test_dissmissed_get(self):
        baker.make(Message)
        msg = baker.make(Message)
        self.check_dismissed(msg, 2, 1)

    def test_not_dissable(self):
        baker.make(Message)
        msg = baker.make(Message, dismissible=False)

        self.check_dismissed(msg, 2, 2)
