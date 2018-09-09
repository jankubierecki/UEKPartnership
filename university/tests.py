from django.test import TestCase
from django.utils import timezone

from university.models import UniversityContactPerson, InstituteUnit, InstituteUnitToUniversityContactPerson


class InstituteUnitCreationTestCase(TestCase):

    def setUp(self):
        self.institute_unit = InstituteUnit(name='institute', created_at=timezone.now())

    def test_institute_unit_created(self):
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
