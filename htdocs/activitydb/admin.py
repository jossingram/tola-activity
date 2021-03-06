from django.contrib import admin
from .models import Country, Province, Office, Village, Program, ProgramAdmin, Documentation, Template,District, Sector, \
     ProgramDashboard, CustomDashboard, ProjectAgreement, ProjectAgreementAdmin,ProjectComplete, ProjectCompleteAdmin, SiteProfile, Capacity, Monitor, \
    Benchmarks, Evaluate, ProjectType, ProjectTypeOther, TrainingAttendance, Beneficiary, Budget, ProfileType, FAQ, ApprovalAuthority, \
    ApprovalAuthorityAdmin, ChecklistItem, ChecklistItemAdmin,Checklist, ChecklistAdmin, DocumentationApp, ProvinceAdmin, DistrictAdmin, AdminLevelThree, AdminLevelThreeAdmin, StakeholderType, Stakeholder, \
    Contact, StakeholderAdmin, ContactAdmin, FormLibrary, FormLibraryAdmin, FormEnabled, FormEnabledAdmin, Feedback, FeedbackAdmin
from import_export import resources
from import_export.admin import ImportExportModelAdmin


class ProjectAgreementResource(resources.ModelResource):

    class Meta:
        model = ProjectAgreement
        widgets = {
                'create_date': {'format': '%d/%m/%Y'},
                'edit_date': {'format': '%d/%m/%Y'},
                'expected_start_date': {'format': '%d/%m/%Y'},
                }


class ProjectAgreementAdmin(ImportExportModelAdmin):
    resource_class = ProjectAgreementResource
    pass

admin.site.register(Country)
admin.site.register(Province, ProvinceAdmin)
admin.site.register(Office)
admin.site.register(District, DistrictAdmin)
admin.site.register(AdminLevelThree, AdminLevelThreeAdmin)
admin.site.register(Village)
admin.site.register(Program, ProgramAdmin)
admin.site.register(CustomDashboard)
admin.site.register(Sector)
admin.site.register(ProgramDashboard)
admin.site.register(ProjectAgreement, ProjectAgreementAdmin)
admin.site.register(ProjectComplete, ProjectCompleteAdmin)
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
admin.site.register(ApprovalAuthority, ApprovalAuthorityAdmin)
admin.site.register(ChecklistItem, ChecklistItemAdmin)
admin.site.register(Checklist, ChecklistAdmin)
admin.site.register(DocumentationApp)
admin.site.register(Stakeholder, StakeholderAdmin)
admin.site.register(Contact, ContactAdmin)
admin.site.register(StakeholderType)
admin.site.register(FormLibrary,FormLibraryAdmin)
admin.site.register(FormEnabled,FormEnabledAdmin)
admin.site.register(Feedback,FeedbackAdmin)







