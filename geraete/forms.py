from django import forms
from django.forms.models import ModelChoiceIterator
from geraete import models


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = models.Employee
        fields = [
            "first_name",
            "last_name",
            "prof_group",
            "is_instructor",
        ]


class DeviceForm(forms.ModelForm):
    class Meta:
        model = models.Device
        fields = [
            "category",
            "vendor",
            "name",
        ]


class CustomModelChoiceIterator(ModelChoiceIterator):
    def choice(self, obj):
        # import pdb; pdb.set_trace()
        return (
            self.field.prepare_value(obj),
            self.field.label_from_instance(obj),
            obj,
            self.field.widget.checked_attribute.get("checked", False),
        )


class CustomModelChoiceField(forms.ModelMultipleChoiceField):
    def _get_choices(self):
        if hasattr(self, "_choices"):
            return self._choices
        return CustomModelChoiceIterator(self)

    choices = property(_get_choices, forms.MultipleChoiceField._set_choices)


class ProfessionalGroupForm(forms.ModelForm):
    devices = CustomModelChoiceField(
        widget=forms.CheckboxSelectMultiple,
        queryset=models.Device.objects.all()
        .order_by("category")
        .select_related("category"),
    )

    class Meta:
        model = models.ProfessionalGroup
        fields = "__all__"


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


class InstructorDevicesForm(forms.ModelForm):
    class Meta:
        model = models.Employee
        fields = ["instructor_for"]
