from django.contrib import admin

from .models import ProjectStatus, ProjectStatusAdmin, Gallery, GalleryAdmin, ProgramLinks,ProgramLinksAdmin, Link, LinkAdmin

admin.site.register(ProjectStatus, ProjectStatusAdmin)
admin.site.register(Gallery, GalleryAdmin)
admin.site.register(ProgramLinks, ProgramLinksAdmin)
admin.site.register(Link, LinkAdmin)







