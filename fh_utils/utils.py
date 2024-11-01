from datetime import date
from typing import ClassVar

from dateutil.easter import easter


class ModelStatus:
    LIVE_STATUS = 1
    DRAFT_STATUS = 2
    HIDDEN_STATUS = 3

    STATUS_CHOICES: ClassVar[list[tuple[int, str]]] = [
        (LIVE_STATUS, "Published"),
        (HIDDEN_STATUS, "Unpublished"),
        (DRAFT_STATUS, "Draft"),
    ]

    @classmethod
    def get_name(cls, status):
        return " ".join([s[1] for s in cls.STATUS_CHOICES if s[0] == status])


def next_easter() -> date:
    today = date.today()
    easter_date = easter(today.year)
    if easter_date < today:
        easter_date = easter(today.year + 1)

    return easter_date


def is_easter() -> bool:
    today = date.today()
    return today == easter(today.year)
