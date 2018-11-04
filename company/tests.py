from django.db import transaction
from django.test import TestCase
from unittest import mock

from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.utils import timezone

from company.models import Company, CompanyContactPerson, EmailInformedUsers
from .signals import company_email_changed, company_contact_person_email_changed

from django.core import mail


class CompanyCreationTestCase(TestCase):
    def setUp(self):
        """ company initialization with proper arguments """

        self.company = Company(name='example', created_at=timezone.now(), email='example@example.com',
                               website='https://www.example.com', krs_code=1111111111,
                               nip_code=1111111111)

    def test_company_created(self):
        """ tests if company was created correctly with proper arguments"""

        self.company.save()

        self.assertIsNotNone(Company.objects.get(id=self.company.id))

    def test_company_not_created_without_argument(self):
        """ tests if creation fails when argument is not provided"""

        try:
            with transaction.atomic():
                self.company.name = None
                self.company.save()
        except IntegrityError:
            pass
        else:
            self.fail()

    def test_company_updated(self):
        """ tests if object was updated correctly """

        self.company.save()

        try:
            with transaction.atomic():
                self.company.name = 'company'
                self.company.save()
        except Exception:
            self.fail()
        else:
            self.assertTrue(self.company.name == 'company')

    def test_company_not_updated(self):
        """ tests if object was not updated with wrong arguments """

        self.company.save()

        try:
            with transaction.atomic():
                self.company.nip_code = ''
                self.company.full_clean()
                self.company.save()
        except Exception:
            assert True

        self.company = Company.objects.get(id=self.company.id)

        self.assertEqual(self.company.nip_code, '1111111111')

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


class CompanySignalTriggeredTestCase(TestCase):
    """ tests if signal was properly triggered"""

    def setUp(self):
        self.company = Company(name='example', created_at=timezone.now(), email='example@gmail.com',
                               website='https://www.example.com', krs_code=1111111111,
                               nip_code=1111111111)

    @mock.patch('company.models.Company.save')
    def test_company_creation_signal_triggered(self, mocked):
        """ tests if mocked was triggered"""

        self.company.save()

        self.assertTrue(mocked.called)
        self.assertEqual(mocked.call_count, 1)

    @mock.patch('company.models.Company.save')
    def test_company_creation_signal_not_triggered(self, mocked):
        """ tests if signal was not triggered with bad parameters """

        try:
            with transaction.atomic():
                self.company.nip_code = ''
                self.company.full_clean()
                self.company.save()
        except Exception as e:
            print(e)

        self.assertFalse(mocked.called)
        self.assertEqual(mocked.call_count, 0)

    def tearDown(self):
        Company.objects.all().delete()


class CompanyContactPersonSignalTriggeredTestCase(TestCase):
    """ tests if signal was properly triggered"""

    def setUp(self):
        self.company_contact_person = CompanyContactPerson(first_name='example', last_name='example',
                                                           email='example@example.com')

    @mock.patch('company.models.CompanyContactPerson.save')
    def test_company_creation_signal_triggered(self, mocked):
        """ tests if singal was propely triggered """

        self.company_contact_person.save()

        self.assertTrue(mocked.called)
        self.assertEqual(mocked.call_count, 1)

    @mock.patch('company.models.CompanyContactPerson.save')
    def test_company_creation_signal_not_triggered(self, mocked):
        """ tests if singal was not triggered with wrong parameters """

        try:
            with transaction.atomic():
                self.company_contact_person.email = ""
                self.company_contact_person.full_clean()
                self.company_contact_person.save()
        except ValidationError as e:
            print(e)

        self.assertFalse(mocked.called)
        self.assertEqual(mocked.call_count, 0)

    def tearDown(self):
        CompanyContactPerson.objects.all().delete()


class CatchSignal:
    def __init__(self, signal):
        self.signal = signal
        self.handler = mock.Mock()

    def __enter__(self):
        self.signal.connect(self.handler)
        return self.handler

    def __exit__(self, exc_type, exc_value, tb):
        self.signal.disconnect(self.handler)


class TestCompanyContentSignalTestCase(TestCase):
    """ tests if signal was properly triggered with args"""

    def setUp(self):
        self.company = Company(name='example', created_at=timezone.now(), email='example@gmail.com',
                               website='https://www.example.com', krs_code=1111111111,
                               nip_code=1111111111)

    def test_signal_with_arguments(self, **kwargs):
        with CatchSignal(company_email_changed) as handler:
            self.company.save()
        handler.assert_called_once_with(
            company=self.company,
            sender=mock.ANY,
            signal=company_email_changed

        )

    def tearDown(self):
        Company.objects.all().delete()


class TestCompanyContactPersonContentSignalTestCase(TestCase):
    """ tests if signal was properly triggered with args"""

    def setUp(self):
        self.company_contact_person = CompanyContactPerson(first_name='example', last_name='example',
                                                           email='example@example.com')

    def test_signal_with_arguments(self, **kwargs):
        with CatchSignal(company_contact_person_email_changed) as handler:
            self.company_contact_person.save()
        handler.assert_called_once_with(
            company_contact_person=self.company_contact_person,
            sender=mock.ANY,
            signal=company_contact_person_email_changed
        )

    def tearDown(self):
        CompanyContactPerson.objects.all().delete()


class TestCompanyEmailSendTestCase(TestCase):
    def setUp(self):
        self.company = Company(name='example', created_at=timezone.now(), email='example@example.com',
                               website='https://www.example.com', krs_code=1111111111,
                               nip_code=1111111111)

    def test_email_with_parameters(self):
        """ tests if email contains proper parameters """

        self.company.save()

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject,
                         ' Powiadomienie o gromadzeniu danych osobowych firmy ' + self.company.name)

    def test_company_informed(self):
        """ tests if company is in the EmailInformedUsers list """

        self.company.save()

        informed = EmailInformedUsers.objects.get(email='example@example.com')
        self.assertIsNotNone(informed)

    def test_company_not_informed(self):
        """ tests if company has not been added twice to EmailInformedUsers list """

        self.company.save()

        Company.objects.create(name='example2', created_at=timezone.now(),
                               email='example@example.com',
                               website='https://www.example.com', krs_code=1111111111,
                               nip_code=1111111111)

        informed_users = EmailInformedUsers.objects.filter(email__icontains='example').count()

        self.assertEquals(informed_users, 1)

    def tearDown(self):
        Company.objects.all().delete()


class TestCompanyContactPersonEmailSendTestCase(TestCase):
    """ tests if email parameters are correct """

    def setUp(self):
        self.company_contact_person = CompanyContactPerson(first_name='example', last_name='example',
                                                           email='example@example.com')

    def test_company_contact_person_informed(self):
        """ tests if company is in the EmailInformedUsers list """

        self.company_contact_person.save()

        informed = EmailInformedUsers.objects.get(email='example@example.com')
        self.assertIsNotNone(informed)

    def test_company_contact_person_not_informed(self):
        """ tests if company has not been added twice to EmailInformedUsers list """

        self.company_contact_person.save()

        self.company_contact_person = CompanyContactPerson(first_name='example', last_name='example',
                                                           email='example@example.com')

        informed_users = EmailInformedUsers.objects.filter(email__icontains='example').count()

        self.assertEquals(informed_users, 1)

    def test_email_with_parameters(self):
        """ tests if email contains proper parameters """

        self.company_contact_person.save()

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject,
                         ' Powiadomienie o gromadzeniu danych osobowych uzytkownika ' + self.company_contact_person.first_name)

    def tearDown(self):
        CompanyContactPerson.objects.all().delete()
