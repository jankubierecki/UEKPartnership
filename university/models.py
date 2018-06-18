from django.db import models

from . import validators


class InstituteUnit(models.Model):
    name = models.CharField("Nazwa", max_length=255)
    created_at = models.DateTimeField("Utworzono", auto_now_add=True)
    updated_at = models.DateTimeField("Zaktualizowano", auto_now=True)
    university_contact_persons = models.ManyToManyField("UniversityContactPerson",
                                                        through="InstituteUnitToUniversityContactPerson")

    def __str__(self):
        return "%s" % self.name

    class Meta:
        verbose_name = "Jednostka Współpracująca UEK"
        verbose_name_plural = "Jednostki Współpracujące UEK"
        ordering = ["name"]


class UniversityContactPerson(models.Model):
    first_name = models.CharField("Imię", max_length=255)
    last_name = models.CharField("Nazwisko", max_length=255)
    phone = models.CharField("Telefon", max_length=50, blank=True, null=True)
    email = models.EmailField("Email", max_length=50,
                              validators=[validators.email_validation], help_text="Tylko z domeną UEK")
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
            self.institute_unit.name, self.university_contact_person.first_name,
            self.university_contact_person.last_name)

    class Meta:
        verbose_name = "Przypisana osoba"
        verbose_name_plural = "Przypisane osoby"
        ordering = ["-created_at"]
