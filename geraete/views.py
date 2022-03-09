from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.text import slugify
from django.views.decorators.http import require_POST
from geraete import forms
from geraete.models import (
    Employee,
    Device,
    ProfessionalGroup,
    Instruction,
    PrimaryInstruction,
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
        emp.save_from_post(
            request.session.get("company_id"),
            request.POST.getlist("prof_group"),
        )
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
        emp.save_from_post(
            request.session.get("company_id"),
            request.POST.getlist("prof_group"),
        )
        return redirect("employees")
    devices = (
        emp.instructor_for.all()
        .order_by("category__category", "vendor", "name")
        .select_related("category")
    )
    return render(
        request,
        "geraete/employee_edit.html",
        {"form": form, "employee": emp, "devices": devices},
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
    if id is not None:
        pg = get_object_or_404(company_s(request, ProfessionalGroup), id=id)
        checked_devices = pg.devices.all()
    else:
        pg, checked_devices = None, []
    form = forms.ProfessionalGroupForm(request.POST or None, instance=pg)
    if form.is_valid():
        pg = form.save(commit=False)
        pg.save_from_post(
            request.session.get("company_id"), request.POST.getlist("devices")
        )
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
        save_c(form, request.session["company_id"])
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
def primaryinstructions(request):
    pis = company_s(request, PrimaryInstruction).order_by(
        "day", "device_company"
    )
    return render(
        request,
        "geraete/primaryinstructions.html",
        {"pi_s": pis},
    )


@login_required
def primaryinstruction(request, id=None):
    """Create or edit a PrimaryInstruction

    Can be called by
    - GET without id: new PrimaryInstruction
    - GET with id: edit PrimaryInstruction
    - POST without id: save new PrimaryInstruction
    - POST with id: save edited PrimaryInstruction

    """
    if id is None:
        pi = None
    else:
        pi = get_object_or_404(
            PrimaryInstruction,
            id=id,
            company_id=request.session.get("company_id"),
        )

    if request.method == "POST":
        form = forms.PrimaryInstructionForm(request.POST, instance=pi)
        emp_selected = map(int, request.POST.getlist("instructed"))
        dev_selected = map(int, request.POST.getlist("devices"))

        if form.is_valid():
            if id is None:
                pi = save_c(form, request.session["company_id"])
            else:
                pi = form.save()
            pi.instructed.add(*emp_selected)
            pi.devices.add(*dev_selected)
            pi.save_instructor_status()
            return redirect("/")
    elif pi is not None:
        emp_selected = pi.instructed.values_list("id", flat=True)
        dev_selected = pi.devices.values_list("id", flat=True)
        form = forms.PrimaryInstructionForm(instance=pi)
    else:
        emp_selected, dev_selected = [], []
        form = forms.PrimaryInstructionForm()

    instructed_qs = (
        company_s(request, Employee)
        .order_by("last_name", "first_name")
        .prefetch_related("prof_group")
    )
    instructed = [
        (emp, emp.classes(), emp.id in emp_selected) for emp in instructed_qs
    ]
    devices = [
        (dev, slugify(dev.vendor), dev.id in dev_selected)
        for dev in company_s(request, Device)
        .order_by("vendor", "name")
        .select_related("category")
    ]
    vendors = []
    lastslug = ""
    for device, slug, _ in devices:
        if slug != lastslug:
            vendors.append((slug, device.vendor))
            lastslug = slug
    return render(
        request,
        "geraete/primaryinstruction_form.html",
        {
            "form": form,
            "instructed": instructed,
            "devices": devices,
            "pi": pi,
            "vendors": vendors,
            "profgroups": company_s(request, ProfessionalGroup).order_by(
                "name"
            ),
        },
    )


@require_POST
@login_required
def get_devices(request):
    """Return a partial view of the devices for an instructor

    Should be called by POST, usually by htmx
    """
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
        "employees", "devices", "devices__category"
    )
    employees = {}
    to_instruct = {}
    for pg in pgs:
        pg_devs = list(pg.devices.all())
        for emp in pg.employees.all():
            employees[emp.id] = emp
            to_instruct[emp.id] = set(pg_devs)
    for instr in Instruction.objects.all().prefetch_related(
        "instructed", "devices"
    ):
        devices = set(instr.devices.all())
        for emp in instr.instructed.all():
            if emp.id in to_instruct:
                to_instruct[emp.id] -= devices
    data = [
        (emp, sorted(to_instruct[emp.id], key=lambda x: str(x)))
        for emp in employees.values()
    ]
    return render(request, "geraete/lacking_instructions.html", {"data": data})
