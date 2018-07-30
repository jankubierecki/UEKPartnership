import re

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def email_validation(email):
    reg = '^[_a-z0-9-]+(\.[_a-z0-9-]+)*@uek.krakow.pl$'
    if not re.match(reg, email):
        raise ValidationError(
            _('Email musi kończyć się na @uek.krakow.pl'),
        )
