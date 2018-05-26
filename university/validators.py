import re

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from validate_email import validate_email


def email_validation(email):
    is_valid = validate_email(email)
    reg = '^[_a-z0-9-]+@uek.krakow.pl$'
    if not re.match(reg, email) or not is_valid:
        raise ValidationError(
            _('email powinien kończyć się @uek.krakow.pl'),
        )
