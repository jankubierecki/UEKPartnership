from django.conf import settings
from django.core.validators import EmailValidator
from django.db import models


# wydzial
class UniversityFaculty(models.Model):
    name = models.CharField("Nazwa", max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Wydział"
        verbose_name_plural = "Wydziały"
        ordering = ["name"]


# katedra
class Institute(models.Model):
    name = models.CharField("Nazwa", max_length=255)
    university_faculty = models.ForeignKey(UniversityFaculty, on_delete=models.CASCADE,
                                           related_name="institutes", verbose_name="Wydział")

    def __str__(self):
        return "[%s] %s" % (self.university_faculty.name, self.name)

    class Meta:
        verbose_name = "Katedra"
        verbose_name_plural = "Katedry"
        ordering = ["name"]


# jednostka wspolpracujaca
class InstituteUnit(models.Model):
    name = models.CharField("Nazwa", max_length=255)
    institute = models.ForeignKey(Institute, on_delete=models.SET_NULL, blank=True, null=True,
                                  related_name="institute_units", verbose_name="Katedra")
    created_at = models.DateTimeField("Utworzono", auto_now_add=True)
    updated_at = models.DateTimeField("Zaktualizowano", auto_now=True)
    university_contact_persons = models.ManyToManyField("UniversityContactPerson",
                                                        through="InstituteUnitToUniversityContactPerson")

    def __str__(self):
        if self.institute is not None:
            return "[%s] %s" % (self.institute.name, self.name)
        else:
            return "[brak wydziału] %s" % self.name

    class Meta:
        verbose_name = "Jednostka Współpracująca UEK"
        verbose_name_plural = "Jednostki Współpracujące UEK"
        ordering = ["institute__name", "name"]


# jednostka do kontaktu UEK
class UniversityContactPerson(models.Model):
    first_name = models.CharField("Imię", max_length=255)
    last_name = models.CharField("Nazwisko", max_length=255)
    phone = models.CharField("Telefon", max_length=50, blank=True, null=True)
    email = models.EmailField("Email", max_length=50, blank=True, null=True,
                              validators=[EmailValidator(whitelist=settings.WHITELISTED_EMAIL_NAMES)])
    academic_title = models.CharField("Tytuł naukowy", max_length=50, blank=True, null=True)
    created_at = models.DateTimeField("Utworzono", auto_now_add=True)
    updated_at = models.DateTimeField("Zaktualizowano", auto_now=True)

    def __str__(self):
        return "%s %s" % (self.first_name, self.last_name)

    class Meta:
        verbose_name = "Osoba do kontaktu UEK"
        verbose_name_plural = "Osoby do kontaktu UEK"
        ordering = ["last_name", "first_name"]


class InstituteUnitToUniversityContactPerson(models.Model):
    institute_unit = models.ForeignKey(InstituteUnit, verbose_name="Jednostka Współpracująca UEK",
                                       on_delete=models.CASCADE)
    university_contact_person = models.ForeignKey(UniversityContactPerson, on_delete=models.CASCADE,
                                                  verbose_name="Osoba do kontaktu UEK", related_name="institute_units")
    created_at = models.DateTimeField("Utworzono", auto_now_add=True)

    def __str__(self):
        return "%s - %s %s" % (
        self.institute_unit.name, self.university_contact_person.first_name, self.university_contact_person.last_name)

    class Meta:
        verbose_name = "Przypisana katedra"
        verbose_name_plural = "Przypisane katedry"
        ordering = ["-created_at"]
