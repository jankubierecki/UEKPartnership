import re

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_krs(krs):
    reg = '^(\d{10})$'
    if not re.match(reg, krs):
        raise ValidationError(
            _('To nie jest prawidłowy numer krs'),
        )


def validate_zip(zip_code):
    reg = '\d{2}-\d{3}'
    if not re.match(reg, zip_code):
        raise ValidationError(
            _('podaj prawidłowy kod pocztowy, np 30-362'),
        )


def validate_nip(zip_code):
    reg = '^(\d{10})$'
    if not re.match(reg, zip_code):
        raise ValidationError(
            _('To nie jest prawidłowy numer krs'),
        )
