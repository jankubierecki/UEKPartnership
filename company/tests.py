from django.test import TestCase
from unittest import mock

from django.core.exceptions import ValidationError

from company.models import Company, CompanyContactPerson
from .signals import *


class CompanyCreationTestCase(TestCase):
    def setUp(self):
        """ company creation with proper arguments """

        self.company = Company.objects.create(name='example', created_at=timezone.now(), email='example@example.com',
                                              website='https://www.example.com', krs_code=1111111111,
                                              nip_code=1111111111)

    def test_company_created_raises_validation_error(self):
        """ tests if validation error works correctly"""

        self.assertRaises(ValidationError, self.company.full_clean())

    def test_company_created(self):
        """ tests if company was created correctly with proper arguments"""

        self.company.full_clean()

        self.assertIsNotNone(Company.objects.filter(pk=self.company.pk))

    def test_company_validation_email_created(self):
        """ tests email validation """

        cases = ["", 1, "example", "example.com", "example@example@.com", "example@.com", "@.com",
                 "example.", "www.example.com"]

        for case in cases:
            self.company.email = case
            try:
                self.company.full_clean()
            except ValidationError as e:
                self.assertTrue('email' in e.message_dict)
            else:
                print("wrong email passed the test ", self.company.email)
                self.assertTrue(1 == 0)

    def test_company_validation_website_created(self):
        """ tests website validation """

        cases = ["", 1, "example", "example.com", "example@example@.com", "example@.com", "@.com",
                 "example.", "www.example.com"]

        for case in cases:
            self.company.website = case
            try:
                self.company.full_clean()
            except ValidationError as e:
                self.assertTrue('website' in e.message_dict)
            else:
                print("wrong website passed the test ", self.company.website)
                self.assertTrue(1 == 0)

    def test_company_validation_krs_code_created(self):
        """ tests krs_code validation """

        cases = [" ", "", 1, "example", 111111111, '1-11111111', '111a1111111', ]

        for case in cases:
            self.company.krs_code = case
            try:
                self.company.full_clean()
            except ValidationError as e:
                self.assertTrue('krs_code' in e.message_dict)
            else:
                print("wrong krs_code passed the test ", self.company.krs_code)
                self.assertTrue(1 == 0)

    def test_company_validation_zip_code_created(self):
        """ tests zip_code validation """

        cases = [" ", 1, "example", '30-3623', 111111, '1-1112', 'ab-aaa', ]

        for case in cases:
            self.company.zip_code = case
            try:
                self.company.full_clean()
            except ValidationError as e:
                self.assertTrue('zip_code' in e.message_dict)
            else:
                print("wrong zip_code passed the test ", self.company.zip_code)
                self.assertTrue(1 == 0)

    def tearDown(self):
        Company.objects.all().delete()


class CompanySignalTriggeredTestCase():
    """ tests if signal was properly triggered"""

    def setUp(self):
        self.company = Company.objects.create(name='example', created_at=timezone.now(), email='example@gmail.com',
                                              website='https://www.example.com', krs_code=1111111111,
                                              nip_code=1111111111)

    @mock.patch('company.models.Company.save')
    def test_company_creation_signal_triggered(self, mocked):
        """ tests if mocked was triggered"""

        self.assertTrue(mocked.called)
        self.assertEqual(mocked.call_count, 1)

    @mock.patch('company.models.Company.save')
    def test_company_creation_signal_not_triggered(self, mocked):
        """ tests if mocked was triggered when wrong krs_code was given"""

        self.company.krs_code = ""

        try:
            self.company.full_clean()
        except ValidationError as e:
            self.assertFalse(mocked.called)
            self.assertEqual(mocked.call_count, 0)

    def tearDown(self):
        Company.objects.all().delete()


class CompanyContactPersonSignalTriggeredTestCase():
    """ tests if signal was properly triggered"""

    def setUp(self):
        self.company_contact_person = CompanyContactPerson.objects.create(first_name='example', last_name='example',
                                                                          email='example@example.com')

    @mock.patch('company.models.CompanyContactPerson.save')
    def test_company_creation_signal_triggered(self, mocked):

        self.assertTrue(mocked.called)
        self.assertEqual(mocked.call_count, 1)

    @mock.patch('company.models.CompanyContactPerson.save')
    def test_company_creation_signal_not_triggered(self, mocked):
        """ tests if mocked was triggered when wrong email was given"""

        self.company_contact_person.email = ""

        try:
            self.company_contact_person.full_clean()
        except ValidationError as e:
            self.assertFalse(mocked.called)
            self.assertEqual(mocked.call_count, 0)

    def tearDown(self):
        CompanyContactPerson.objects.all().delete()

