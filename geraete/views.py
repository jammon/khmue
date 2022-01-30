from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from geraete import models, forms


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
    form = forms.EmployeeForm(request.POST or None)
    if form.is_valid():
        form.save()
        form = forms.EmployeeForm()
    employees = (
        models.Employee.objects.all()
        .order_by(
            "prof_group__name", "-is_instructor", "last_name", "first_name"
        )
        .select_related("prof_group")
    )
    return render(
        request,
        "geraete/employees.html",
        {"employees": employees, "form": form},
    )


@login_required
def employee_edit(request, id):
    emp = get_object_or_404(models.Employee, id=id)
    form = forms.EmployeeForm(request.POST or None, instance=emp)
    if form.is_valid():
        form.save()
        return redirect("employees")
    return render(
        request,
        "geraete/employee_edit.html",
        {"form": form, "employee": emp},
    )


# Devices ===================================================================
@login_required
def devices(request):
    devices = models.Device.objects.select_related("category").order_by(
        "category__category", "vendor", "name"
    )
    return render(
        request,
        "geraete/devices.html",
        {
            "devices": devices,
            "device_form": forms.DeviceForm(),
        },
    )


@login_required
def device_add(request):
    form = forms.DeviceForm(request.POST or None)
    if form.is_valid():
        form.save()
        form = forms.DeviceForm()
    devices = models.Device.objects.select_related("category").order_by(
        "category__category", "vendor", "name"
    )
    return render(
        request,
        "geraete/partials/devices_list.html",
        {
            "device_form": form,
            "devices": devices,
        },
    )


# Professional Groups =========================================================
@login_required
def prof_groups(request):
    return render(
        request,
        "geraete/prof_groups.html",
        {"groups": models.ProfessionalGroup.objects.order_by("name")},
    )


@login_required
def prof_group(request, id=None):
    """Edit Professional Group

    Can be called by GET with id: show form for ProfGroup
    … by GET without id: show empty form
    … by POST with id: update ProfGroup
    … by POST without id: save ProfGroup
    """
    if id:
        pg = get_object_or_404(models.ProfessionalGroup, id=id)
        checked_devices = pg.devices.all()
    else:
        pg = None
    form = forms.ProfessionalGroupForm(request.POST or None, instance=pg)
    if form.is_valid():
        form.save()
        return redirect("prof_groups")
    devices = []
    for device in (
        models.Device.objects.all()
        .select_related("category")
        .order_by("category__category", "vendor", "name")
    ):
        devices.append((device, id is not None and device in checked_devices))
    return render(
        request,
        "geraete/prof_group_form.html",
        {"prof_group_form": form, "prof_group": pg, "devices": devices},
    )


# Instructions ================================================================
@login_required
def instruction(request):
    form = forms.InstructionForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect("/")
    devices = (
        models.Device.objects.filter(
            instructors__id=form.cleaned_data.get("instructor")
        )
        if hasattr(form, "cleaned_data")
        else None
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
        pi = form.save()
        # save instructor status
        devices = pi.devices.all()
        for empl in pi.instructed.filter(is_instructor=True):
            empl.instructor_for.add(devices)
        return redirect("/")
    return render(
        request,
        "geraete/primaryinstruction_form.html",
        {"form": form},
    )


@login_required
def get_devices(request):
    devices = models.Device.objects.filter(
        instructors__id=int(request.POST.get("instructor"))
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
    pgs = models.ProfessionalGroup.objects.all().prefetch_related(
        "employee_set", "devices"
    )
    employees = {}
    to_instruct = {}
    for pg in pgs:
        pg_devs = list(pg.devices.all())
        for emp in pg.employee_set.all():
            employees[emp.id] = emp
            to_instruct[emp.id] = set(pg_devs)
    for instr in models.Instruction.objects.all().prefetch_related(
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
