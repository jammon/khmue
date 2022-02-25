from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.text import slugify
from geraete import forms
from geraete.models import (
    Employee,
    Device,
    ProfessionalGroup,
    Instruction,
    company_s,
    save_c,
)


@login_required
def index(request):
    return render(request, "geraete/index.html", {})


def login(request):
    return render(
        request, "geraete/login.html", {"form": AuthenticationForm()}
    )


# Employees ===================================================================
@login_required
def employees(request):
    company_id = request.session.get("company_id")
    form = forms.EmployeeForm(request.POST or None)
    if form.is_valid():
        emp = form.save(commit=False)
        emp.save_from_post(request)
        form = forms.EmployeeForm()
    return render(
        request,
        "geraete/employees.html",
        {
            "employees": company_s(company_id, Employee)
            .order_by("last_name", "first_name")
            .prefetch_related("prof_group"),
            "form": form,
        },
    )


@login_required
def employee_edit(request, id):
    company_id = request.session.get("company_id")
    emp = get_object_or_404(Employee, id=id, company__id=company_id)
    if request.POST:
        for key, value in request.POST.items():
            print(f"{key=}, {value=} ")
    print(f"prof_group: {request.POST.getlist('prof_group')} ")
    form = forms.EmployeeForm(request.POST or None, instance=emp)
    if form.is_valid():
        emp = form.save(commit=False)
        emp.save_from_post(request)
        return redirect("employees")
    return render(
        request,
        "geraete/employee_edit.html",
        {"form": form, "employee": emp},
    )


# Devices ===================================================================
@login_required
def devices(request):
    return render(
        request,
        "geraete/devices.html",
        {
            "devices": Device.get_sorted(request),
            "device_form": forms.DeviceForm(),
        },
    )


@login_required
def device_add(request):
    form = forms.DeviceForm(request.POST or None)
    if form.is_valid():
        save_c(form, request.session["company_id"])
        form = forms.DeviceForm()
    return render(
        request,
        "geraete/partials/devices_list.html",
        {
            "device_form": form,
            "devices": Device.get_sorted(request),
        },
    )


# Professional Groups =========================================================
@login_required
def prof_groups(request):
    return render(
        request,
        "geraete/prof_groups.html",
        {"groups": company_s(request, ProfessionalGroup).order_by("name")},
    )


@login_required
def prof_group(request, id=None):
    """Edit Professional Group

    Can be called by GET with id: show form for ProfGroup
    … by GET without id: show empty form
    … by POST with id: update ProfGroup
    … by POST without id: save ProfGroup
    """
    company_id = request.session["company_id"]
    if id:
        pg = get_object_or_404(company_s(request, ProfessionalGroup), id=id)
        checked_devices = pg.devices.all()
    else:
        pg, checked_devices = None, []
    form = forms.ProfessionalGroupForm(request.POST or None, instance=pg)
    if form.is_valid():
        pg = form.save(commit=False)
        pg.save_from_post(request)
        return redirect("prof_groups")
    devices = [
        (device, device in checked_devices)
        for device in Device.get_sorted(request)
    ]
    return render(
        request,
        "geraete/prof_group_form.html",
        {"form": form, "prof_group": pg, "devices": devices},
    )


# Instructions ================================================================
@login_required
def instruction(request):
    form = forms.InstructionForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect("/")
    devices = None
    if hasattr(form, "cleaned_data"):
        devices = Device.objects.filter(
            instructors__id=form.cleaned_data.get("instructor")
        )
    return render(
        request,
        "geraete/instruction_form.html",
        {"form": form, "devices": devices},
    )


@login_required
def primaryinstruction(request):
    form = forms.PrimaryInstructionForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect("/")
    emp_selected = (int(emp) for emp in request.POST.getlist("employees"))
    employees = [
        (
            emp,
            " ".join([f"pg_{pg.id}" for pg in emp.prof_group.all()]),
            emp.id in emp_selected,
        )
        for emp in company_s(request, Employee)
        .order_by("last_name", "first_name")
        .prefetch_related("prof_group")
    ]
    dev_selected = (int(dev) for dev in request.POST.getlist("devices"))
    devices = [
        (dev, slugify(dev.vendor), dev.id in dev_selected)
        for dev in company_s(request, Device).order_by("vendor", "name")
    ]
    return render(
        request,
        "geraete/primaryinstruction_form.html",
        {
            "form": form,
            "employees": employees,
            "devices": devices,
        },
    )


@login_required
def get_devices(request):
    devices = Device.get_for_instructor(
        int(request.POST.get("instructor")), request.session["company_id"]
    )
    return render(
        request,
        "geraete/partials/instructor_devices.html",
        {"devices": devices},
    )


@login_required
def lacking_instructions(request, employee_id=None, profgroup_id=None):
    """List all employees and their count of missing instructions

    retrieve
      - all prof_groups with employees and devices
      - all instructions
    """
    pgs = ProfessionalGroup.objects.all().prefetch_related(
        "employee_set", "devices"
    )
    employees = {}
    to_instruct = {}
    for pg in pgs:
        pg_devs = list(pg.devices.all())
        for emp in pg.employee_set.all():
            employees[emp.id] = emp
            to_instruct[emp.id] = set(pg_devs)
    for instr in Instruction.objects.all().prefetch_related(
        "instructed", "devices"
    ):
        for emp in instr.instructed.all():
            if emp.id in to_instruct:
                to_instruct[emp.id] -= set(instr.devices.all())
    data = [
        (emp, sorted(to_instruct[emp.id], key=lambda x: str(x)))
        for emp in employees.values()
    ]
    return render(request, "geraete/lacking_instructions.html", {"data": data})
