# Django
from django.test import TestCase
from django.urls import reverse

# Third Party
from model_bakery import baker

# First Party
from site_messages.models import Message
from site_messages.templatetags.message_tags import messages


class TestSiteMessages(TestCase):
    def test_key(self):
        msg = baker.make(Message)
        self.assertEqual(msg.session_key, f"message-{msg.slug}-dismissed")

    def test_dismiss_session(self):
        msg = baker.make(Message)

        session = self.client.session

        self.assertIsNone(session.get(msg.session_key))
        msg.dismiss(session)
        self.assertTrue(session.get(msg.session_key))

    def test_dismiss_view(self):
        msg = baker.make(Message)

        self.assertIsNone(self.client.session.get(msg.session_key))
        self.client.get(msg.dismiss_url)
        self.assertTrue(self.client.session.get(msg.session_key))

    def test_dismiss_url(self):
        msg = baker.make(Message)
        msg_url = reverse("site_messages:dismiss", kwargs={"slug": msg.slug})
        self.assertEqual(msg.dismiss_url, msg_url)

    def check_dismissed(self, msg, before, after):
        session = self.client.session
        self.assertEqual(len(Message.get_messages(session)), before)
        msg.dismiss(session)
        self.assertEqual(len(Message.get_messages(session)), after)

    def test_dismissed_get(self):
        baker.make(Message)
        msg = baker.make(Message)
        self.check_dismissed(msg, 2, 1)

    def test_not_disable(self):
        baker.make(Message)
        msg = baker.make(Message, dismissible=False)

        self.check_dismissed(msg, 2, 2)

    def test_str(self):
        msg = baker.make(Message)

        self.assertEqual(f"{msg}", msg.title)

    def test_message_tag(self):
        msgs = []
        for _ in range(5):
            msgs.append(baker.make(Message))

        class MockContext:
            def __init__(self, request) -> None:
                self.request = request

        context = MockContext(self.client)

        self.assertEqual(messages(context), {"messages": msgs})
