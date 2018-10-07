from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.test import TestCase
from django.utils import timezone

from university.models import UniversityContactPerson, InstituteUnit, InstituteUnitToUniversityContactPerson


class InstituteUnitCreationTestCase(TestCase):

    def setUp(self):
        self.institute_unit = InstituteUnit(name='institute', created_at=timezone.now())

    def test_institute_unit_created_with_contact_person(self):
        """ tests if institute unit created with company_contact_person """

        #  Given
        self.university_contact_person = UniversityContactPerson(first_name='test', last_name='example',
                                                                 email='test@test.com')

        self.institute_unit.save()
        self.university_contact_person.save()

        # When
        self.institute_to_contact_person = InstituteUnitToUniversityContactPerson.objects.create(
            institute_unit=self.institute_unit, university_contact_person=self.university_contact_person,
            created_at=timezone.now())

        # Then
        self.assertEqual(self.institute_unit.university_contact_persons.get(first_name='test'),
                         self.university_contact_person)

        self.assertEqual(self.university_contact_person.institute_units.get(institute_unit=self.institute_unit),
                         self.institute_to_contact_person)

        self.assertIsNotNone(InstituteUnitToUniversityContactPerson.objects.get(institute_unit=self.institute_unit))

        self.assertIsNotNone(InstituteUnit.objects.get(university_contact_persons=self.university_contact_person))

    def tearDown(self):
        InstituteUnit.objects.all().delete()
        UniversityContactPerson.objects.all().delete()
        InstituteUnitToUniversityContactPerson.objects.all().delete()


class UniversityContactPersonTestCase(TestCase):

    def setUp(self):
        self.university_contact_person = UniversityContactPerson(first_name='test', last_name='test',
                                                                 email='test@uek.krakow.pl')

    def test_university_contact_person_created(self):
        """ tests if object was created with proper arguments """

        # When
        self.university_contact_person.full_clean()
        self.university_contact_person.save()

        # Then
        self.assertEqual(UniversityContactPerson.objects.get(pk=self.university_contact_person.pk),
                         self.university_contact_person)


class InstituteUnitToUniversityContactPersonTestCase(TestCase):

    def setUp(self):
        self.university_contact_person = UniversityContactPerson(first_name='test', last_name='test',
                                                                 email='test@uek.krakow.pl')
        self.institute_unit = InstituteUnit(name='institute', created_at=timezone.now())

    def test_contact_already_registered(self):
        """ tests if two or more the same contact person cannot be registered as a contacts """

        # Given
        self.institute_unit.save()
        self.university_contact_person.save()

        # When
        self.institute_to_contact_person = InstituteUnitToUniversityContactPerson.objects.create(
            institute_unit=self.institute_unit, university_contact_person=self.university_contact_person,
            created_at=timezone.now())

        # Then
        with self.assertRaises(IntegrityError) as ie:
            InstituteUnitToUniversityContactPerson.objects.create(
                institute_unit=self.institute_unit,
                university_contact_person=self.university_contact_person,
                created_at=timezone.now())

        self.assertTrue('duplicate key value violates unique constraint' in str(ie.exception))
