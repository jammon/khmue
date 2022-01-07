from django.db import models
from datetime import date

# Create your models here.


class DeviceCat(models.Model):
    category = models.CharField("Kategorie", max_length=50)

    class Meta:
        verbose_name = "Gerätekategorie"
        verbose_name_plural = "Gerätekategorien"

    def __str__(self):
        return self.category


class Device(models.Model):
    category = models.ForeignKey(
        DeviceCat, on_delete=models.CASCADE, verbose_name="Kategorie"
    )
    vendor = models.CharField("Hersteller", max_length=50)
    name = models.CharField("Name", max_length=50)

    class Meta:
        verbose_name = "Gerät"
        verbose_name_plural = "Geräte"

    def __str__(self):
        return f"{self.category}: {self.name} von {self.vendor} "


class ProfessionalGroup(models.Model):
    name = models.CharField("Name", max_length=50)
    devices = models.ManyToManyField(
        Device,
        verbose_name="Einzuweisende Geräte",
    )

    class Meta:
        verbose_name = "Berufsgruppe"
        verbose_name_plural = "Berufsgruppen"

    def __str__(self):
        return self.name


class Employee(models.Model):
    title = models.CharField("Titel", max_length=20, null=True, blank=True)
    first_name = models.CharField("Vorname", max_length=50)
    last_name = models.CharField("Nachname", max_length=50)
    prof_group = models.ForeignKey(
        ProfessionalGroup,
        on_delete=models.CASCADE,
        verbose_name="Berufsgruppe",
        null=True,
        blank=True,
    )
    company = models.CharField("Firma", max_length=50, default="KHMUE")
    is_instructor = models.BooleanField(
        default=False, verbose_name="MPG-Beauftragter"
    )
    instructor_for = models.ManyToManyField(
        Device, verbose_name="Einweiser für", related_name="instructors"
    )

    class Meta:
        verbose_name = "Mitarbeiter"
        verbose_name_plural = "Mitarbeiter"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Instruction(models.Model):
    day = models.DateField("Datum", default=date.today)
    instructor = models.ForeignKey(
        Employee,
        verbose_name="Einweiser",
        on_delete=models.PROTECT,
        limit_choices_to={"is_instructor": True},
        related_name="held_instructions",
    )
    instructed = models.ManyToManyField(
        Employee, verbose_name="Eingewiesene", related_name="instructions"
    )
    # TODO: limit to devices for this instructor
    devices = models.ManyToManyField(
        Device, verbose_name="Geräte", related_name="instructions"
    )

    class Meta:
        verbose_name = "Einweisung"
        verbose_name_plural = "Einweisungen"

    def __str__(self):
        return f"Einweisung am {self.day.strftime('%d.%m.%y')} "


class PrimaryInstruction(models.Model):
    day = models.DateField("Datum", default=date.today)
    instructor = models.CharField("Einweiser", max_length=50)
    device_company = models.CharField("Firma", max_length=50)
    instructed = models.ManyToManyField(
        Employee,
        verbose_name="Eingewiesene",
        related_name="primaryinstructions",
    )
    devices = models.ManyToManyField(
        Device, verbose_name="Geräte", related_name="primaryinstructions"
    )

    class Meta:
        verbose_name = "Ersteinweisung"
        verbose_name_plural = "Ersteinweisungen"

    def __str__(self):
        return f"Ersteinweisung am {self.day.strftime('%d.%m.%y')} "
