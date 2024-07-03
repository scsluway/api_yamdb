import re

from rest_framework.exceptions import ValidationError


def regex_validator(value):
    if value.lower() == 'me':
        raise ValidationError('Username "me" is not allowed.')

    invalid_chars = ''.join(set(re.sub(r'^[\w.@+-]+\Z', '', value)))
    if invalid_chars:
        error_message = (f'Username contains invalid characters:'
                         f' {invalid_chars}')
        raise ValidationError(error_message)
    return value


class UsernameValidationMixin:
    def validate_username(self, value):
        return regex_validator(value)