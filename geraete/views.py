from django.shortcuts import (
    render,
    redirect,
    get_object_or_404,
)
from geraete import models, forms


def index(request):
    devices = models.Device.objects.all().order_by(
        "category__category", "vendor", "name"
    )
    employees = (
        models.Employee.objects.all()
        .order_by("prof_group__name", "is_instructor")
        .select_related("prof_group")
    )
    instructions = (
        models.Instruction.objects.all()
        .order_by("-day")
        .select_related("instructor")
    )
    return render(
        request,
        "geraete/index.html",
        {
            "devices": devices,
            "employees": employees,
            "employee_form": forms.EmployeeForm(),
            "instructions": instructions,
        },
    )


def employees(request):
    employees = (
        models.Employee.objects.all()
        .order_by("prof_group__name", "is_instructor")
        .select_related("prof_group")
    )
    return render(
        request,
        "geraete/employees.html",
        {
            "employees": employees,
            "employee_form": forms.EmployeeForm(),
        },
    )


def employee_add(request):
    form = forms.EmployeeForm(request.POST or None)
    if form.is_valid():
        form.save()
        form = forms.EmployeeForm()
    employees = (
        models.Employee.objects.all()
        .order_by("prof_group__name", "is_instructor")
        .select_related("prof_group")
    )
    return render(
        request,
        "geraete/employees_list.html",
        {
            "employee_form": form,
            "employees": employees,
        },
    )


def employee_edit(request, id):
    emp = get_object_or_404(models.Employee, id=id) if id else None
    form = forms.EmployeeForm(request.POST or None, instance=emp)
    if form.is_valid():
        form.save()
        return redirect("employees")
    return render(
        request,
        "geraete/employee_edit.html",
        {
            "employee_form": form,
            "employee": emp,
        },
    )


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
        "geraete/devices_list.html",
        {
            "device_form": form,
            "devices": devices,
        },
    )


def prof_groups(request):
    return render(
        request,
        "geraete/prof_groups.html",
        {"groups": models.ProfessionalGroup.objects.order_by("name")},
    )


def prof_group(request, id=None):
    """Edit Professional Group

    Can be called by GET with id: show form for ProfGroup
    … by GET without id: show empty form
    … by POST with id: update ProfGroup
    … by POST without id: save ProfGroup
    """
    pg = get_object_or_404(models.ProfessionalGroup, id=id) if id else None
    form = forms.ProfessionalGroupForm(request.POST or None, instance=pg)
    if form.is_valid():
        form.save()
        return redirect("prof_groups")
    return render(
        request,
        "geraete/prof_group_form.html",
        {
            "prof_group_form": form,
            "prof_group": pg,
        },
    )


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


def get_devices(request):
    devices = models.Device.objects.filter(
        instructors__id=int(request.POST.get("instructor"))
    )
    return render(
        request,
        "geraete/instructor_devices.html",
        {"devices": devices},
    )


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
