# Standard Library
from collections.abc import Callable

# Django
from django.http import HttpRequest, HttpResponse
from secure import Secure


class ClacksOverhead:
    def __init__(self, get_response: Callable[[HttpRequest], HttpResponse]):
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        response = self.get_response(request)
        response["X-Clacks-Overhead"] = "GNU Terry Pratchett"

        return response


secure_headers = Secure.with_default_headers()


class SecureHeaders:
    def __init__(self, get_response: Callable[[HttpRequest], HttpResponse]):
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        response = self.get_response(request)
        csp = response.headers["Content-Security-Policy"]
        secure_headers.set_headers(response)  # type: ignore
        response["Content-Security-Policy"] = csp

        return response
