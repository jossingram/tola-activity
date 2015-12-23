from django.db import models
from django.contrib import admin
from django.conf import settings
from activitydb.models import Program
from datetime import datetime


LINK_TYPE_CHOICES = (
    ('gallery', 'Gallery'),
    ('map', 'MapBox Map Layer'),
)


class ProjectStatus(models.Model):
    project_status = models.CharField("Project Status", max_length=50, blank=True)
    description = models.CharField("Status Description", max_length=200, blank=True)
    create_date = models.DateTimeField(null=True, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)

    def __unicode__(self):
        return self.program__name


class ProjectStatusAdmin(admin.ModelAdmin):
    list_display = ('project_status','description','create_date','edit_date')
    display = 'Project Status'


class ProgramNarrative(models.Model):
    program = models.ForeignKey(Program, blank=True)
    description = models.TextField("Status Description", max_length=200, blank=True)
    create_date = models.DateTimeField(null=True, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)

    def __unicode__(self):
        return '%s' % (self.program)


class ProgramNarrativeAdmin(admin.ModelAdmin):
    list_display = ('program','create_date','edit_date')
    display = 'Program Narrative'


class Link(models.Model):
    link = models.CharField("Link to Service", max_length=200, blank=True)
    create_date = models.DateTimeField(null=True, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)

    def __unicode__(self):
        return self.link


class LinkAdmin(admin.ModelAdmin):
    list_display = ('link','create_date','edit_date')
    display = 'Link'


class ProgramLinks(models.Model):
    program = models.ForeignKey(Program, blank=True)
    type = models.CharField("Type of Link",blank=True, null=True, max_length=255, choices=LINK_TYPE_CHOICES)
    link = models.ForeignKey(Link, max_length=200, blank=True)
    create_date = models.DateTimeField(null=True, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)

    def __unicode__(self):
        return '%s' % (self.program)


class ProgramLinksAdmin(admin.ModelAdmin):
    list_display = ('program','create_date','edit_date')
    display = 'Program Links'



