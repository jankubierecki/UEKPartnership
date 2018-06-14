from django.db import models

from company.models import Company, CompanyContactPerson
from university.models import InstituteUnit, UniversityContactPerson


class Contract(models.Model):
    contract_date = models.DateField("Data zawiązania umowy")
    amount = models.FloatField("Kwota w złotówkach", null=True, blank=True)
    contract_number = models.CharField("Numer umowy", max_length=100)
    additional_info = models.TextField("Dodatkowe Informacje", null=True, blank=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="contracts",
                                verbose_name="Firmy")
    partnership = models.OneToOneField("Partnership", on_delete=models.SET_NULL, null=True, related_name="contract",
                                       verbose_name="Współprace")
    institute_unit = models.ForeignKey(InstituteUnit, on_delete=models.SET_NULL, null=True,
                                       related_name="contracts",
                                       verbose_name="Jednostki Współpracujące")

    def __str__(self):
        return "%s %s" % (self.contract_number, self.company.name)

    class Meta:
        verbose_name = "Umowa"
        verbose_name_plural = "Umowy"
        ordering = ["-contract_date"]


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
        ("paid_and_on", "Opłacona - w trakcie"),
        ("started_not_paid", "Nieopłacona - w trakcie"),
        ("other", "Inna")
    )

    company_contact_person = models.ForeignKey(CompanyContactPerson, on_delete=models.SET_NULL,
                                               null=True,
                                               related_name="partnerships", verbose_name="Osoby Do kontaktu Firmy")
    university_contact_person = models.ForeignKey(UniversityContactPerson, on_delete=models.SET_NULL,
                                                  null=True,
                                                  related_name="partnerships", verbose_name="Osoby Do kontaktu UEK")
    contract_date = models.DateField("Data rozpoczęcia współpracy")
    last_contact_date = models.DateField("Rok ostatniego kontaktu")
    name = models.CharField("Nazwa współpracy", max_length=255, default="bla")
    type_of_partnership = models.CharField("Typ współpracy", max_length=255, choices=TYPES_OF_PARTNERSHIPS,
                                           default=TYPES_OF_PARTNERSHIPS[1][0])
    kind_of_partnership = models.CharField("Rodzaj współpracy", max_length=255, choices=KINDS_OF_PARTNERSHIPS,
                                           default=KINDS_OF_PARTNERSHIPS[1][0])
    status = models.CharField("Status", max_length=255, choices=STATUS_OF_PARTNERSHIP, default=STATUS_OF_PARTNERSHIP[2][0])

    def __str__(self):
        return "%s %s" % (self.contract.contract_number, self.contract.company.name)

    class Meta:
        verbose_name = "Współpraca"
        verbose_name_plural = "Współprace"
        ordering = ["-contract_date"]
