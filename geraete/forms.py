from django import forms
from geraete import models


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = models.Employee
        fields = [
            "title",
            "first_name",
            "last_name",
            "prof_group",
            "is_instructor",
        ]
        widgets = {
            "prof_group": forms.CheckboxSelectMultiple,
        }


class DeviceForm(forms.ModelForm):
    class Meta:
        model = models.Device
        fields = [
            "category",
            "vendor",
            "name",
        ]


class ProfessionalGroupForm(forms.ModelForm):
    class Meta:
        model = models.ProfessionalGroup
        fields = ["name", "devices"]


class InstructionForm(forms.ModelForm):
    class Meta:
        model = models.Instruction
        fields = "__all__"
        widgets = {
            "instructor": forms.RadioSelect(
                attrs={
                    "hx-post": "/get_devices",
                    "hx-target": "#devices",
                    "hx-swap": "innerHTML",
                }
            )
        }


class PrimaryInstructionForm(forms.ModelForm):
    class Meta:
        model = models.PrimaryInstruction
        fields = "__all__"
        widgets = {
            "instructed": forms.CheckboxSelectMultiple,
            "devices": forms.CheckboxSelectMultiple,
        }


class InstructorDevicesForm(forms.ModelForm):
    class Meta:
        model = models.Employee
        fields = ["instructor_for"]
