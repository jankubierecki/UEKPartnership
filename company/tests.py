from django.test import TestCase
from unittest import mock

from company.models import Company, CompanyContactPerson
from .signals import *


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
