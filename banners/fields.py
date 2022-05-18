# Standard Library
import contextlib

# Django
from django.db import models


class DayMonthField(models.DateField):
    def __init__(self, *args, **kwargs):
        try:
            self.after = kwargs["after"]
            del kwargs["after"]
        except KeyError:
            self.after = None

        super().__init__(*args, **kwargs)

    @staticmethod
    def get_base_year():
        return 2000

    def get_year(self, model_instance):
        year = self.get_base_year()

        if self.after is not None:
            after = model_instance.__dict__[self.after]
            year = after.year
            if after > model_instance.__dict__[self.name].replace(year=year):
                year = after.year + 1

        return year

    def pre_save(self, model_instance, add):
        year = self.get_year(model_instance)
        value = super().pre_save(model_instance, add)
        with contextlib.suppress(AttributeError):
            value = value.replace(year=year)
        model_instance.__dict__[self.name] = value

        return value
