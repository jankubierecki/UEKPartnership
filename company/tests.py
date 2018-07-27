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
        companies = Company.objects.all()
        del companies


class SignalTriggeredTestCase(TestCase):
    """ tests if signal was properly triggered"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    @mock.patch('company.models.Company.save')
    def test_company_creation_signal_triggered(self, mocked):
        self.company = Company.objects.create(name='Intel', created_at=timezone.now(), email='jankubierecki@gmail.com',
                                              website='intel.com', krs_code=1111111111, nip_code=1111111111)
        self.assertTrue(mocked.called)

        self.assertEqual(mocked.call_count, 1)

    @mock.patch('company.models.CompanyContactPerson.save')
    def test_company_contact_person_creation_signal_triggered(self, mocked):
        self.company_contact_person = CompanyContactPerson.objects.create(first_name='Robert', last_name='Steve',
                                                                          email='rs@gmail.com')
        self.assertTrue(mocked.called)

        self.assertEqual(mocked.call_count, 1)


class CompanyEmailContextVariablesTestCase(TestCase):
    """ tests variables in templated mail context """

    def setUp(self):
        pass

    def tearDown(self):
        pass

    @mock.patch('company.models.Company.save')
    def test_company_email_context_variables(self, mocked):
        self.company = Company.objects.create(name='Intel', created_at=timezone.now(), email='jankubierecki@gmail.com',
                                              website='intel.com', krs_code=1111111111, nip_code=1111111111)
        kwargs = mocked
        context = kwargs['context']

        self.assertEqual(context['company_name'], self.company.name)


class CompanyContactPersonEmailContextVariablesTestCase(TestCase):
    """ tests variables in templated mail context """

    def setUp(self):
        pass

    def tearDown(self):
        pass

    @mock.patch('company.models.CompanyContactPerson.save')
    def test_company_email_context_variables(self, send_templated_mail):
        self.company_contact_person = CompanyContactPerson.objects.create(first_name='Robert', last_name='Steve',
                                                                          email='rs@gmail.com')
        kwargs = send_templated_mail.call_args[1]
        context = kwargs['context']

        self.assertEqual(context['company_contact_person_name'], self.company_contact_person.name)


class CompanyEmailShouldNotifyTestCase(TestCase):
    """ tests if unit should have been noticed """

    def setUp(self):
        pass

    def tearDown(self):
        pass


class CompanyContactPersonShouldNotifyTestCase(TestCase):
    """ tests if unit should have been noticed """

    def setUp(self):
        pass

    def tearDown(self):
        pass
