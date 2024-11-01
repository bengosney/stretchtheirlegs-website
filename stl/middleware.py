from collections.abc import Callable

from secure import Secure

from django.http import HttpRequest, HttpResponse


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
        csp = response.headers.get("Content-Security-Policy")
        secure_headers.set_headers(response)  # type: ignore
        if csp:
            response["Content-Security-Policy"] = csp
        else:
            response.headers.pop("Content-Security-Policy", None)

        return response
