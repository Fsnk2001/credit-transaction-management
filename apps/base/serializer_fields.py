from rest_framework import serializers

from .validators import (
    contains_number_validator,
    contains_letter_validator,
    contains_special_char_validator,
    phone_number_validator,
)


class PasswordField(serializers.CharField):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def validate(self, value):
        contains_number_validator(value)
        contains_letter_validator(value)
        contains_special_char_validator(value)
        return value


class PhoneNumberField(serializers.CharField):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def validate(self, value):
        phone_number_validator(value)
        return value
