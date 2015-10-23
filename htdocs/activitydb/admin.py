from django.contrib import admin
from .models import Country, Province, Office, Village, Program, Documentation, Template,District, Sector, \
     ProgramDashboard, ProjectAgreement, ProjectComplete, SiteProfile, Capacity, Monitor, \
    Benchmarks, Evaluate, ProjectType, ProjectTypeOther, TrainingAttendance, Beneficiary, Budget, ProfileType, FAQ, ApprovalAuthority, \
    ChecklistItem, DocumentationApp, ProvinceAdmin, DistrictAdmin, AdminLevelThree, AdminLevelThreeAdmin


admin.site.register(Country)
admin.site.register(Province, ProvinceAdmin)
admin.site.register(Office)
admin.site.register(District, DistrictAdmin)
admin.site.register(AdminLevelThree, AdminLevelThreeAdmin)
admin.site.register(Village)
admin.site.register(Program)
admin.site.register(Sector)
admin.site.register(ProgramDashboard)
admin.site.register(ProjectAgreement)
admin.site.register(ProjectComplete)
admin.site.register(Documentation)
admin.site.register(Template)
admin.site.register(SiteProfile)
admin.site.register(Capacity)
admin.site.register(Monitor)
admin.site.register(Benchmarks)
admin.site.register(Evaluate)
admin.site.register(ProjectType)
admin.site.register(ProjectTypeOther)
admin.site.register(TrainingAttendance)
admin.site.register(Beneficiary)
admin.site.register(Budget)
admin.site.register(ProfileType)
admin.site.register(FAQ)
admin.site.register(ApprovalAuthority)
admin.site.register(ChecklistItem)
admin.site.register(DocumentationApp)


