import pytest
from django.test import Client, TestCase

from geraete.forms import EmployeeForm
from geraete.models import (
    Company,
    Device,
    DeviceCat,
    Employee,
    PrimaryInstruction,
    company_s,
    save_c,
)


@pytest.mark.django_db
def test_company_s():
    c1 = Company.objects.create(name="C1")
    c2 = Company.objects.create(name="C2")
    d11 = DeviceCat.objects.create(company=c1, category="d11")
    d12 = DeviceCat.objects.create(company=c1, category="d12")
    d21 = DeviceCat.objects.create(company=c2, category="d21")
    qs = company_s(c1.id, DeviceCat)
    assert d11 in qs
    assert d12 in qs
    assert d21 not in qs

    class MockRequest(object):
        def __init__(self, session):
            self.session = session

    request = MockRequest({"company_id": c1.id})
    qs = company_s(request, DeviceCat)
    assert d11 in qs
    assert d12 in qs
    assert d21 not in qs


@pytest.mark.django_db
def test_save_c_with_employee():
    employee = Employee(
        title="Dr.",
        first_name="Heinz",
        last_name="Müller",
        is_instructor=False,
    )
    form = EmployeeForm(instance=employee)
    c = Company.objects.create(name="C")
    emp = save_c(form, c.id)
    assert isinstance(emp, Employee)
    assert emp.title == "Dr."
    assert emp.first_name == "Heinz"
    assert emp.last_name == "Müller"
    assert emp.is_instructor == False
    assert emp.company_id == c.id


class TestPrimaryInstruction(TestCase):
    fixtures = ["all.json"]

    def test_instructors(self):
        company_id = 1
        instructor_id = 1
        device_id = 2
        devices = Device.get_for_instructor(instructor_id, company_id)
        assert len(devices) == 1
        assert devices[0].id == 1
        pi = PrimaryInstruction.objects.create(
            company_id=company_id,
            instructor="Heinz Draeger",
            device_company="Draeger",
        )
        pi.instructed.add(instructor_id)
        pi.devices.add(device_id)
        pi.save_instructor_status()
        devices = Device.get_for_instructor(instructor_id, company_id)
        assert len(devices) == 2
        assert set([d.id for d in devices]) == set([1, 2])
