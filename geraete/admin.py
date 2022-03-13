from django.contrib import admin

from geraete.models import (
    Company,
    Device,
    DeviceCat,
    Employee,
    Instruction,
    PrimaryInstruction,
    ProfessionalGroup,
    SiteUser,
)

admin.site.register(DeviceCat)
admin.site.register(Device)
admin.site.register(ProfessionalGroup)
admin.site.register(Employee)
admin.site.register(Instruction)
admin.site.register(PrimaryInstruction)
admin.site.register(SiteUser)
admin.site.register(Company)
