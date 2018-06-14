from django.db import models
from company.signals import company_contact_person_email_changed, company_email_changed

from . import validators


class Company(models.Model):
    name = models.CharField("Nazwa", max_length=255)
    phone = models.CharField("Telefon", max_length=50, blank=True, null=True)
    created_at = models.DateTimeField("Utworzono", auto_now_add=True)
    email = models.CharField("Email do firmy", max_length=50, default=" ")
    updated_at = models.DateTimeField("Zaktualizowano", auto_now=True)
    website = models.URLField("Strona Internetowa")
    city = models.CharField("Miasto", max_length=64, blank=True)
    street = models.CharField("Ulica", max_length=64, blank=True)
    zip_code = models.CharField("Kod pocztowy", max_length=6, null=True, blank=True,
                                validators=[validators.validate_zip])
    industry = models.CharField("Branża", max_length=64, blank=True)
    company_size = models.CharField("Wielkość firmy", max_length=64, blank=True)
    krs_code = models.CharField("Numer KRS", max_length=10, blank=False, null=False,
                                validators=[validators.validate_krs])
    nip_code = models.CharField("Numer NIP", max_length=10, default=" ", validators=[validators.validate_nip])
    company_contact_persons = models.ManyToManyField("CompanyContactPerson", through="CompanyToCompanyContactPerson",
                                                     related_name="companies")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Firma"
        verbose_name_plural = "Firmy"
        ordering = ["name"]

    def email_has_changed(self):
        return self.email != Company.objects.filter(id=self.id).values_list(['email'], flat=True)[0]

    def save(self, *args, **kwargs):
        should_notify = self.id is None or self.email_has_changed()
        super(Company, self).save(*args, **kwargs)
        if should_notify:
            company_email_changed.send(sender=Company, company=self)


class CompanyContactPerson(models.Model):
    first_name = models.CharField("Imię", max_length=255)
    last_name = models.CharField("Nazwisko", max_length=255)
    phone = models.CharField("Telefon", max_length=50, blank=True, null=True)
    email = models.EmailField("Email", max_length=50, default=" ")
    created_at = models.DateTimeField("Utworzono", auto_now_add=True)
    updated_at = models.DateTimeField("Zaktualizowano", auto_now=True)

    def __str__(self):
        return "%s %s" % (self.first_name, self.last_name)

    class Meta:
        verbose_name = "Osoba do kontaktu Firmy współpracującej"
        verbose_name_plural = "Osoby do kontaktu Firmy współpracującej"
        ordering = ["last_name", "first_name"]

    def email_has_changed(self):
        return self.email != CompanyContactPerson.objects.filter(id=self.id).values_list('email', flat=True)[0]

    def save(self, *args, **kwargs):
        should_notify = self.id is None or self.email_has_changed()
        super(CompanyContactPerson, self).save(*args, **kwargs)
        if should_notify:
            company_contact_person_email_changed.send(sender=CompanyContactPerson, company_contact_person=self)


class CompanyToCompanyContactPerson(models.Model):
    company = models.ForeignKey(Company, verbose_name="Firma", on_delete=models.CASCADE)
    company_contact_person = models.ForeignKey(CompanyContactPerson, on_delete=models.CASCADE,
                                               verbose_name="Osoba do kontaktu Firmy współpracującej")

    created_at = models.DateTimeField("Utworzono", auto_now_add=True)

    def __str__(self):
        return "%s - %s %s" % (
            self.company.name, self.company_contact_person.first_name,
            self.company_contact_person.last_name)

    class Meta:
        verbose_name = "Przypisana osoba"
        verbose_name_plural = "Przypisane osoby"
        ordering = ["-created_at"]
