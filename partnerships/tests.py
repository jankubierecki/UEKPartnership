from datetime import timedelta
from django.utils import timezone

from django.test import TestCase

from django.core.exceptions import ObjectDoesNotExist

from authorization.models import User
from partnerships.models import Partnership
from partnerships.admin import PartnershipModelForm


class BasePartnershipCreationTestCase(TestCase):
    """ tests for creating partnerships without contracts"""

    def setUp(self):
        self.user = User.objects.create_user('user@test.com', 'test')

        self.partnership = Partnership(start_date=timezone.now(), last_contact_date=timezone.now(), name='example',
                                       type_of_partnership='science', kind_of_partnership='barter', status='other',
                                       author=User.objects.create_user(email='test@test.com', password='test'))

    def test_created_without_contract(self):
        """ tests creation """

        # When
        self.partnership.full_clean()
        self.partnership.save()

        # Then
        self.assertIsNotNone(Partnership.objects.get(id=self.partnership.id))
        self.assertTrue(User.objects.get(id=self.partnership.author.id).id == self.partnership.author.id)

        with self.assertRaises(ObjectDoesNotExist) as e:
            self.partnership.contracts.get()

        self.assertTrue("Contract matching query does not exist" in str(e.exception))

    def test_name_autocomplete_redirect(self):
        """ tests denial anonymous """

        # When
        response = self.client.get('/partnership_autocomplete', follow=True)

        # Then
        self.assertRedirects(response, '/login/?next=/partnership_autocomplete/', status_code=301)

    def test_name_autocomplete_acces(self):
        """ tests if loged user can acces  """

        # Given
        self.client.force_login(self.user, backend=None)

        # When
        response = self.client.get('/partnership_autocomplete', follow=True)

        # Then
        self.assertEqual(response.status_code, 200)

    def test_name_autocomplete_match(self):
        """ tests if partnership name autocomplete works correctly """

        # Given
        self.partnership.save()
        self.client.force_login(self.user, backend=None)

        # When
        response = self.client.get('/partnership_autocomplete/?term=exa', follow=True)

        # Then
        self.assertContains(response, self.partnership.name, count=1)

    def test_name_autocomplete_not_match(self):
        """ tests if not matches wrong query """

        # Given
        self.partnership.save()
        self.client.force_login(self.user, backend=None)

        # When
        response = self.client.get('/partnership_autocomplete/?term=test', follow=True)

        # Then
        self.assertNotContains(response, self.partnership.name)


class PartnershipDatesTestCase(TestCase):
    """ tests validation of partnership forms dates """

    def setUp(self):
        self.partnership = Partnership.objects.create(start_date=timezone.now(),
                                                      last_contact_date=timezone.now())

    def test_start_older_than_last_contact(self):
        """ start_date must be older than last_contact_date """

        form = PartnershipModelForm(
            data={'start_date': self.partnership.start_date,
                  'last_contact_date': self.partnership.last_contact_date})

        self.assertTrue(form.is_valid())

    def test_start_earlier_than_last_contact_fail(self):
        """ start_date must be older than last_contact_date """

        form = PartnershipModelForm(
            data={'start_date': self.partnership.start_date + timedelta(days=10),
                  'last_contact_date': self.partnership.last_contact_date})

        self.assertFalse(form.is_valid())
        self.assertIn('Data ostatniego kontaktu nie może być starsza od daty rozpoczęcia współpracy',
                      form.errors.get('__all__'))

    def test_start_and_last_contact_less_than_current(self):
        """ if start_date is older than current_date, then last_contact_date must be older too """

        form = PartnershipModelForm(
            data={'start_date': self.partnership.start_date - timedelta(days=10),
                  'last_contact_date': self.partnership.last_contact_date - timedelta(days=10)})

        self.assertTrue(form.is_valid())

    def test_start_and_last_contact_less_than_current_fail(self):
        """ if start_date is older than current_date, then last_contact_date must be older too """

        form = PartnershipModelForm(
            data={'start_date': self.partnership.start_date - timedelta(days=10),
                  'last_contact_date': self.partnership.last_contact_date + timedelta(days=10)})

        self.assertFalse(form.is_valid())
        self.assertIn(
            'Data ostaniego kontaktu nie może wybiegać w przyszłość jeśli data rozpoczęcia jest z przeszłości',
            form.errors.get('__all__'))

    def test_start_and_last_contact_greather_than_current(self):
        """ if both start and last_contact are greater than current, then last_contact == start """

        form = PartnershipModelForm(
            data={'start_date': self.partnership.start_date + timedelta(days=10),
                  'last_contact_date': self.partnership.last_contact_date + timedelta(days=10)})

        self.assertTrue(form.is_valid())

    def test_start_and_last_contact_greather_than_current_fail(self):
        """ if both start and last_contact are greater than current, then last_contact == start """

        form = PartnershipModelForm(
            data={'start_date': self.partnership.start_date + timedelta(days=10),
                  'last_contact_date': self.partnership.last_contact_date + timedelta(days=12)})

        self.assertFalse(form.is_valid())
        self.assertIn(
            'Data ostatniego kontaktu musi być równa dacie rozpoczęcia współpracy jeśli obie są z przyszłości. Ustaw obie daty na ten sam dzień, lub z rezygnuj z przyszłościowych dat',
            form.errors.get('__all__'))


class ContractBaseCreationTestCase(TestCase):
    pass
