from django.core.exceptions import ValidationError


class PublishedDateValidationError(ValidationError):
    def __init__(self, published_from, published_to):
        message = f"published_to({published_to}) can not be before published_from({published_from})"
        super().__init__(message)
