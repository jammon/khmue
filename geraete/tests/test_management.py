from io import StringIO

from django.core.management import call_command
from django.test import TestCase

from geraete.models import Company, Device, DeviceCat, company_s

FILENAME = "geraete/tests/MedGer.csv"


class ImportGeraeteTest(TestCase):
    def test_import_geraete(self):
        company = Company.objects.create(name="Test-KH")
        out = StringIO()
        call_command(
            "import_geraete",
            FILENAME,
            str(company.id),
            stdout=out,
        )
        assert company_s(company.id, DeviceCat).count() == 17
        assert company_s(company.id, Device).count() == 55
        assert f"Geräte aus {FILENAME} importiert." == out.getvalue().strip()
