from django.contrib.auth import get_user_model

from django.db import models

from company.models import Company, CompanyContactPerson
from university.models import InstituteUnit, UniversityContactPerson

from django.core.exceptions import ObjectDoesNotExist


class Partnership(models.Model):
    KINDS_OF_PARTNERSHIPS = (
        ("financial", "Finansowa",),
        ("non_financial", "Niefinansowa",),
        ("barter", "Barterowa",),
        ("sponsored", "Sponsoring")
    )

    TYPES_OF_PARTNERSHIPS = (
        ("science", "Naukowa"),
        ("learning", "Dydaktyczna"),
        ("organizational", "Organizacyjna"),
        ("training", "Szkoleniowa")
    )

    STATUS_OF_PARTNERSHIP = (
        ("finished", "Zakończona"),
        ("unfinished", "W trakcie")
    )

    start_date = models.DateField("Data nawiązania Współpracy")
    last_contact_date = models.DateField("Data ostatniego kontaktu")
    name = models.CharField("Nazwa współpracy", max_length=255,
                            help_text="Po prawej stronie pokażą się współprace o podobnej nazwie, które są już w systemie")
    type_of_partnership = models.CharField("Typ współpracy", max_length=255, choices=TYPES_OF_PARTNERSHIPS,
                                           default=TYPES_OF_PARTNERSHIPS[1][0])
    kind_of_partnership = models.CharField("Rodzaj współpracy", max_length=255, choices=KINDS_OF_PARTNERSHIPS,
                                           default=KINDS_OF_PARTNERSHIPS[1][0])
    status = models.CharField("Status", max_length=255, choices=STATUS_OF_PARTNERSHIP,
                              default=STATUS_OF_PARTNERSHIP[1][0])
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="partnerships",
                                verbose_name="Firma")
    author = models.ForeignKey(get_user_model(), verbose_name="Autor",
                               related_name="partnerships", on_delete=models.SET_NULL, null=True)

    def __str__(self):
        try:
            return "{0}, {1}".format(self.name, self.company.name)
        except ObjectDoesNotExist:
            return "{0}, {1}".format(self.name, 'bez umowy')

    class Meta:
        verbose_name = "Współpraca"
        verbose_name_plural = "Współprace"
        ordering = ["-start_date"]


class Contract(models.Model):
    contract_date = models.DateField("Data zawiązania umowy")
    amount_pay = models.FloatField("Kwota w złotówkach", null=True, blank=True)
    contract_number = models.CharField("Numer umowy", max_length=100)
    additional_info = models.TextField("Dodatkowe Informacje", null=True, blank=True)
    institute_unit = models.ForeignKey(InstituteUnit, on_delete=models.SET_NULL, null=True,
                                       related_name="contracts",
                                       verbose_name="Jednostka Współpracująca")
    partnership = models.ForeignKey(Partnership, on_delete=models.SET_NULL, null=True, blank=True,
                                    related_name="contracts",
                                    verbose_name="Współprace")
    company_contact_persons = models.ManyToManyField(CompanyContactPerson,
                                                     help_text="Osoby do kontaktu firmy związane z tą umową",
                                                     verbose_name='Osoby do kontaktu firmy'
                                                     )

    university_contact_persons = models.ManyToManyField(UniversityContactPerson,
                                                        help_text="Osoby do kontaktu UEK związane z tą umową",
                                                        verbose_name="Osoby do kontaktu UEK"
                                                        )
    created_at = models.DateTimeField("Utworzono", auto_now_add=True)

    def __str__(self):
        return "%s" % self.contract_date

    class Meta:
        verbose_name = "Umowy"
        verbose_name_plural = "Umowy"
        ordering = ["-contract_date"]
        get_latest_by = "created_at"


class PartnershipLogEntry(models.Model):
    created_at = models.DateTimeField("Utworzono", auto_now_add=True)
    updated_at = models.DateTimeField("Zaktualizwoano", auto_now=True)
    description = models.TextField("Opis")
    created_by = models.ForeignKey(get_user_model(), verbose_name="Utworzono przez", related_name="created_log_entries",
                                   on_delete=models.SET_NULL, null=True)
    updated_by = models.ForeignKey(get_user_model(), verbose_name="Zaktualizowano przez",
                                   related_name="updated_log_entries",
                                   on_delete=models.SET_NULL, null=True)
    partnership = models.ForeignKey(Partnership, on_delete=models.SET_NULL,
                                    null=True,
                                    related_name="log_entries", verbose_name="Wspolprace")

    def __str__(self):
        return "%s, %s" % (self.created_at, self.created_by)

    class Meta:
        verbose_name = "Notatka"
        verbose_name_plural = "Notatki"
        ordering = ["updated_by"]
