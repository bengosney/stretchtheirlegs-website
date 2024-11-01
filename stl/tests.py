import pytest

from django.http import HttpRequest, HttpResponse

from stl.middleware import ClacksOverhead, SecureHeaders


@pytest.fixture
def get_response():
    def _get_response(request) -> HttpResponse:
        response = HttpResponse()
        return response

    return _get_response


@pytest.fixture
def get_csp_response():
    def _get_response(request) -> HttpResponse:
        response = HttpResponse()
        response["Content-Security-Policy"] = "default-src 'self'"
        return response

    return _get_response


@pytest.fixture
def secure_headers_middleware(get_response):
    return SecureHeaders(get_response)


@pytest.fixture
def secure_headers_middleware_csp(get_csp_response):
    return SecureHeaders(get_csp_response)


@pytest.fixture
def clacks_overhead_middleware(get_response):
    return ClacksOverhead(get_response)


def test_clacks_overhead_middleware(clacks_overhead_middleware):
    request = HttpRequest()
    response = clacks_overhead_middleware(request)

    assert "X-Clacks-Overhead" in response
    assert response["X-Clacks-Overhead"] == "GNU Terry Pratchett"


def test_secure_headers_are_set(secure_headers_middleware_csp):
    request = HttpRequest()
    response = secure_headers_middleware_csp(request)

    assert "X-Content-Type-Options" in response
    assert "X-Frame-Options" in response
    assert "Strict-Transport-Security" in response


def test_csp_header_is_preserved(secure_headers_middleware_csp):
    request = HttpRequest()
    response = secure_headers_middleware_csp(request)

    assert response["Content-Security-Policy"] == "default-src 'self'"


def test_csp_header_not_set(secure_headers_middleware):
    request = HttpRequest()
    response = secure_headers_middleware(request)

    assert "Content-Security-Policy" not in response
