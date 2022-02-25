from django.contrib import admin

from geraete.models import (
    DeviceCat,
    Device,
    ProfessionalGroup,
    Employee,
    Instruction,
    PrimaryInstruction,
    SiteUser,
    Company,
)

admin.site.register(DeviceCat)
admin.site.register(Device)
admin.site.register(ProfessionalGroup)
admin.site.register(Employee)
admin.site.register(Instruction)
admin.site.register(PrimaryInstruction)
admin.site.register(SiteUser)
admin.site.register(Company)
