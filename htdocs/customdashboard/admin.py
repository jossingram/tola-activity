from django.contrib import admin

from .models import ProjectStatus, ProjectStatusAdmin, ProgramNarrative, ProgramNarrativeAdmin, ProgramLinks, \
    ProgramLinksAdmin, Link, LinkAdmin

class ProgramNarrativeAdmin(admin.ModelAdmin):
    change_form_template = 'customdashboard/admin/change_form.html'


admin.site.register(ProjectStatus, ProjectStatusAdmin)
admin.site.register(ProgramNarrative, ProgramNarrativeAdmin)
admin.site.register(ProgramLinks, ProgramLinksAdmin)
admin.site.register(Link, LinkAdmin)









