from django.db import models
from django.contrib import admin
#from silo.models import Silo



class ReadType(models.Model):
    read_type = models.CharField(max_length=135, blank=True)
    description = models.CharField(max_length=765, blank=True)
    create_date = models.DateTimeField(null=True, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)

    def __unicode__(self):
        return self.read_type


class ReadTypeAdmin(admin.ModelAdmin):
    list_display = ('read_type','description','create_date','edit_date')
    display = 'Read Type'


class Read(models.Model):
    owner = models.ForeignKey('auth.User')
    type = models.ForeignKey(ReadType)
    read_name = models.CharField(max_length=100, blank=True, default='', verbose_name='source name')
    read_url = models.CharField(max_length=100, blank=True, default='', verbose_name='source url')
    description = models.TextField()
    create_date = models.DateTimeField(null=True, blank=True)
    file_data = models.FileField("Upload CSV File", upload_to='uploads', blank=True, null=True)

    class Meta:
        ordering = ('create_date',)

    def save(self, *args, **kwargs):
        super(Read, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.read_name


class ReadAdmin(admin.ModelAdmin):
    list_display = ('owner','read_name','read_url','description','create_date')
    display = 'Read Data Feeds'

