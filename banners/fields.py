# Standard Library
import contextlib
from datetime import datetime

# Django
from django.core.exceptions import FieldDoesNotExist
from django.db import models


class DayMonthField(models.DateField):
    def __init__(self, *args, **kwargs):
        try:
            self.after = kwargs["after"]
            del kwargs["after"]
        except KeyError:
            self.after = None

        super().__init__(*args, **kwargs)

    def get_year(self, model_instance):
        with contextlib.suppress(FieldDoesNotExist, KeyError):
            if model_instance.__dict__[self.after] > model_instance.__dict__[self.name]:
                field = model_instance._meta.get_field(self.after)
                return field.get_year(model_instance) + 1
        return 1970

    def pre_save(self, model_instance, add):
        year = self.get_year(model_instance)
        value = super().pre_save(model_instance, add)
        return value.replace(year=year)

    def from_db_value(self, value, expression, connection):
        return value.replace(year=datetime.now().year)
