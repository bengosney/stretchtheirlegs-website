# Standard Library
import contextlib
import functools
from typing import cast

# Django
from django.db import connection
from django.db.models import Model
from django.db.models.base import ModelBase


class SubclassMixinError(ValueError):
    def __init__(self):
        super().__init__("Subclass must specify mixin")


def clean_models(func):
    @functools.wraps(func)
    def wrapper_clean_models(*args, **kwargs):
        args[0].model.objects.all().delete()
        func(*args, **kwargs)
        return func(*args, **kwargs)

    return wrapper_clean_models


class AbstractModelMixinTestCase:
    """Base class for tests of model mixins/abstract models.

    To use, subclass and specify the mixin class variable. A model using
    the mixin will be made available in self.model
    """

    mixin: type[Model]
    model: type[Model]

    @classmethod
    def setUpClass(cls):
        if cls.mixin is None:
            raise SubclassMixinError()

        cls.model = cast(
            type[Model],
            ModelBase(
                f"__Test{cls.mixin.__name__}",
                (cls.mixin,),
                {"__module__": cls.mixin.__module__},
            ),
        )

        with connection.schema_editor() as schema_editor:
            schema_editor.create_model(cls.model)

        with contextlib.suppress(AttributeError):
            super().setUpClass()

    @classmethod
    def tearDownClass(cls):
        with contextlib.suppress(AttributeError):
            super().tearDownClass()

        with connection.schema_editor() as schema_editor:
            schema_editor.delete_model(cls.model)
