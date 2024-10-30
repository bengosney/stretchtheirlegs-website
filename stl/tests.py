from django.test import TestCase
from django.http import HttpRequest, HttpResponse
import pytest
from stl.middleware import SecureHeaders


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


@pytest.fixture
def get_response():
    def _get_response(request):
        response = HttpResponse()
        response["Content-Security-Policy"] = "default-src 'self'"
        return response

    return _get_response


@pytest.fixture
def secure_headers_middleware(get_response):
    return SecureHeaders(get_response)


def test_secure_headers_are_set(secure_headers_middleware):
    request = HttpRequest()
    response = secure_headers_middleware(request)

    assert "X-Content-Type-Options" in response
    assert "X-Frame-Options" in response
    assert "Strict-Transport-Security" in response


def test_csp_header_is_preserved(secure_headers_middleware):
    request = HttpRequest()
    response = secure_headers_middleware(request)

    assert response["Content-Security-Policy"] == "default-src 'self'"
