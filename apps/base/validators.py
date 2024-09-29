import re

from .exceptions import ValidationError


def contains_number_validator(data: str):
    regex = re.compile('[0-9]')
    if regex.search(data) == None:
        raise ValidationError("Input must include number.")


def contains_letter_validator(data: str):
    regex = re.compile('[a-zA-Z]')
    if regex.search(data) == None:
        raise ValidationError("Input must include letter.")


def contains_special_char_validator(data: str):
    regex = re.compile('[@_!#$%^&*]')
    if regex.search(data) == None:
        raise ValidationError("Input must include special character (@_!#$%^&*).")


def phone_number_validator(data: str):
    regex = re.compile(r'^09\d{9}$')
    if not regex.match(data):
        raise ValidationError("Invalid phone number.")
