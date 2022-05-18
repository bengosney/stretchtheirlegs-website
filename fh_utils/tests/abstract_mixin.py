# Standard Library
import contextlib
from typing import cast

# Django
from django.db import connection
from django.db.models import Model
from django.db.models.base import ModelBase
from django.test.utils import CaptureQueriesContext

# Third Party
from icecream import ic

# from hypothesis.extra.django import TestCase


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
            raise ValueError("Subclass must specify mixin")

        cls.model = cast(
            type[Model],
            ModelBase(
                f"__Test{cls.mixin.__name__}",
                (cls.mixin,),
                {"__module__": cls.mixin.__module__},
            ),
        )

        with CaptureQueriesContext(connection) as ctx:
            with connection.schema_editor() as schema_editor:
                schema_editor.create_model(cls.model)

            ic(ctx.captured_queries)

        with contextlib.suppress(AttributeError):
            super().setUpClass()

    @classmethod
    def tearDownClass(cls):
        with contextlib.suppress(AttributeError):
            super().tearDownClass()

        with connection.schema_editor() as schema_editor:
            schema_editor.delete_model(cls.model)
