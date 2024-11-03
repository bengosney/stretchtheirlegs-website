import pytest

from pages.models import shorten_label


@pytest.fixture(autouse=True)
def use_max_form_title_length(settings):
    settings.MAX_FORM_TITLE_LENGTH = 11


def test_shorten_label_shorter_than_max():
    label = "Short"
    assert shorten_label(label) == "Short"


def test_shorten_label_exactly_max():
    label = "ExactLength"
    assert shorten_label(label) == "ExactLength"


def test_shorten_label_longer_than_max():
    label = "12Characters"
    assert shorten_label(label) == "12Charac..."


def test_shorten_label_much_longer():
    label = "This is a very long label"
    assert shorten_label(label) == "This is..."


def test_shorten_label_empty():
    label = ""
    assert shorten_label(label) == ""
