import argparse
from collections import namedtuple
from django.core.management.base import BaseCommand, CommandError
import csv
from geraete import models


class Command(BaseCommand):
    """Importiert eine Liste von Geräten für ein Krankenhaus

    Die Liste soll eine CSV-Datei sein.
    - erste Spalte: Kategorie
    - zweite Spalte: Typ
    - dritte Spalte: Hersteller
    - letzte Spalte: "1" für einweisungspflichtig
    """

    help = "Importiert eine Liste von Geräten für ein Krankenhaus"

    def add_arguments(self, parser):
        parser.add_argument("csvfile", type=argparse.FileType("r"))
        parser.add_argument("company_id", type=int)

    def handle(self, *args, **options):
        company_id = options["company_id"]
        geraete = set()
        DevTuple = namedtuple("DevTuple", ["kategorie", "typ", "hersteller"])
        with options["csvfile"] as csv_file:
            reader = csv.reader(csv_file)
            for row in reader:
                if int(row[-1]) > 0:
                    geraete.add(DevTuple(*row[:3]))

        kategorien = {}
        for kat in set(ger.kategorie for ger in geraete):
            kategorien[kat] = models.DeviceCat.objects.create(
                company_id=company_id, category=kat
            )

        for kategorie, typ, hersteller in geraete:
            models.Device.objects.create(
                company_id=company_id,
                category=kategorien[kategorie],
                vendor=hersteller,
                name=typ,
            )

        self.stdout.write(
            self.style.SUCCESS(
                f"Geräte aus {options['csvfile'].name} importiert."
            )
        )
