from django.contrib import admin

from .models import ProjectStatus, ProjectStatusAdmin, ProgramNarrative, ProgramNarrativeAdmin, ProgramLinks, \
    ProgramLinksAdmin, Link, LinkAdmin

admin.site.register(ProjectStatus, ProjectStatusAdmin)
admin.site.register(ProgramNarrative, ProgramNarrativeAdmin)
admin.site.register(ProgramLinks, ProgramLinksAdmin)
admin.site.register(Link, LinkAdmin)









