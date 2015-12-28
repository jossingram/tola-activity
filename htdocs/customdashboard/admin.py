from django.contrib import admin
from .models import ProjectStatus, ProjectStatusAdmin, Gallery, GalleryAdmin

admin.site.register(ProjectStatus, ProjectStatusAdmin)
admin.site.register(Gallery,GalleryAdmin)






