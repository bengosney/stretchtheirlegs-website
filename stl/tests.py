# Django
from django.test import TestCase


class ClacksTests(TestCase):
    def test_clacks_overhead(self):
        with self.modify_settings(
            MIDDLEWARE={
                "prepend": "stl.middleware.ClacksOverhead",
                "remove": [
                    "django.contrib.sessions.middleware.SessionMiddleware",
                    "django.contrib.auth.middleware.AuthenticationMiddleware",
                    "django.contrib.messages.middleware.MessageMiddleware",
                ],
            }
        ):
            response = self.client.get("/")

        self.assertTrue(response.has_header("x-clacks-overhead"))
        self.assertEqual(response["x-clacks-overhead"], "GNU Terry Pratchett")
