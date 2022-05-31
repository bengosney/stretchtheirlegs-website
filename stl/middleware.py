# Standard Library
from typing import Callable

# Django
from django.http import HttpRequest, HttpResponse


class ClacksOverhead:
    def __init__(self, get_response: Callable[[HttpRequest], HttpResponse]):
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        response = self.get_response(request)
        response["X-Clacks-Overhead"] = "GNU Terry Pratchett"

        return response
