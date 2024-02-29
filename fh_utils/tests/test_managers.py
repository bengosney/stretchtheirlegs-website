# Standard Library

# Django

# Third Party
from freezegun import freeze_time

# First Party
from fh_utils.managers import DatePeriodManager


def test_leap_year():
    with freeze_time("2024-02-29"):
        DatePeriodManager._get_q()
