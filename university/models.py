from django.db import models


class UniversityFaculty(models.Model):
    name = models.CharField("Nazwa", max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Wydział"
        verbose_name_plural = "Wydziały"
        ordering = ["name"]


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


class InstituteUnit(models.Model):
    name = models.CharField("Nazwa", max_length=255)
    institute = models.ForeignKey(Institute, on_delete=models.SET_NULL, blank=True, null=True,
                                  related_name="instutute_units", verbose_name="Katedra")
    created_at = models.DateTimeField("Utworzono", auto_now_add=True)
    updated_at = models.DateTimeField("Zaktualizowano", auto_now=True)

    def __str__(self):
        if self.institute is not None:
            return "[%s] %s" % (self.institute.name, self.name)
        else:
            return "[brak wydziału] %s" % self.name

    class Meta:
        verbose_name = "Jednostka Współpracująca UEK"
        verbose_name_plural = "Jednostki Współpracująca UEK"
        ordering = ["institute__name", "name"]
