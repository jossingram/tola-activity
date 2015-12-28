from django.db import models
from django.contrib import admin
from django.conf import settings
from datetime import datetime
from activitydb.models import Program, Sector


class ProjectStatus(models.Model):
    project_status = models.CharField("Project Status", max_length=50, blank=True)
    description = models.CharField("Status Description", max_length=200, blank=True)
    create_date = models.DateTimeField(null=True, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)

    def __unicode__(self):
        return self.project_status


class ProjectStatusAdmin(admin.ModelAdmin):
    list_display = ('project_status','description','create_date','edit_date')
    display = 'Project Status'

class Gallery(models.Model):
    program_name = models.ForeignKey(Program, null=True, blank=True)
    title = models.CharField("Title", max_length=100, unique=True)
    narrative = models.TextField("Narrative Text", blank=True)
    image_name = models.CharField("Image URL", max_length=50, blank=True)
    create_date = models.DateTimeField(null=True, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)

    def __unicode__(self):
        return self.title

class GalleryAdmin(admin.ModelAdmin):
    list_display = ('title','narrative','image_name','create_date','edit_date')
    display = 'Photo Gallery'

