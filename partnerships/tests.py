from django.db import transaction
from django.test import TestCase

from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.utils import timezone

from .models import Contract, Partnership, PartnershipLogEntry


class ContractTestCase(TestCase):

    def setUp(self):
        pass
