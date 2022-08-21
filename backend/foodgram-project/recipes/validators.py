from django.conf import settings
from django.core.exceptions import ValidationError

MESSAGES = getattr(settings, "MESSAGES", None)


def validator_not_zero(value):
    if value == 0:
        raise ValidationError(MESSAGES["greater_zero"])
