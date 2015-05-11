from django.db import models
from django.contrib import admin
from django.conf import settings
from silo.models import Silo
from activitydb.models import Program, Sector, Community, ProjectAgreement
from datetime import datetime



class IndicatorType(models.Model):
    indicator_type = models.CharField(max_length=135, blank=True)
    description = models.CharField(max_length=765, blank=True)
    create_date = models.DateTimeField(null=True, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)

    def __unicode__(self):
        return self.indicator_type


class IndicatorTypeAdmin(admin.ModelAdmin):
    list_display = ('indicator_type','description','create_date','edit_date')
    display = 'Indicator Type'

class DisaggregationType(models.Model):
    disaggregation_type = models.CharField(max_length=135, blank=True)
    description = models.CharField(max_length=765, blank=True)
    create_date = models.DateTimeField(null=True, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)

    def __unicode__(self):
        return self.disaggregation_type


class DisaggregationTypeAdmin(admin.ModelAdmin):
    list_display = ('disaggregation_type','description','create_date','edit_date')
    display = 'Disaggregation Type'


class ReportingFrequency(models.Model):
    frequency= models.CharField(max_length=135, blank=True)
    description = models.CharField(max_length=765, blank=True)
    create_date = models.DateTimeField(null=True, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)

    def __unicode__(self):
        return self.disaggregation_type


class ReportingFrequencyAdmin(admin.ModelAdmin):
    list_display = ('frequency','description','create_date','edit_date')
    display = 'Reporting Frequency'


class Indicator(models.Model):
    owner = models.ForeignKey('auth.User')
    indicator_type = models.ForeignKey(IndicatorType, null=True, blank=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    number = models.CharField(max_length=255, null=True, blank=True)
    source = models.CharField(max_length=255, null=True, blank=True)
    definition = models.CharField(max_length=255, null=True, blank=True)
    disaggregation = models.ForeignKey(DisaggregationType, null=True, blank=True)
    baseline = models.CharField(max_length=255, null=True, blank=True)
    lop_target = models.CharField(max_length=255, null=True, blank=True)
    means_of_verification = models.CharField(max_length=255, null=True, blank=True)
    data_collection_method = models.CharField(max_length=255, null=True, blank=True)
    responsible_person = models.CharField(max_length=255, null=True, blank=True)
    method_of_analysis = models.CharField(max_length=255, null=True, blank=True)
    information_use = models.CharField(max_length=255, null=True, blank=True)
    reporting_frequency = models.ForeignKey(ReportingFrequency, null=True, blank=True)
    comments = models.CharField(max_length=255, null=True, blank=True)
    program = models.ManyToManyField(Program)
    sector = models.ForeignKey(Sector)
    approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, related_name="approving_indicator")
    approval_submitted_by = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, related_name="indicator_submitted_by")
    create_date = models.DateTimeField(null=True, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ('create_date',)

    def save(self, *args, **kwargs):
        #onsave add create date or update edit date
        if self.create_date == None:
            self.create_date = datetime.now()
        self.edit_date = datetime.now()
        super(Indicator, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name


class IndicatorAdmin(admin.ModelAdmin):
    list_display = ('owner','indicator_type','name','sector','description', 'program')
    display = 'Indicators'


class CollectedData(models.Model):
    targeted = models.CharField("Targeted #", max_length=255, blank=True, null=True)
    achieved = models.CharField("Achieved #", max_length=255, blank=True, null=True)
    description = models.CharField("Description", max_length=255, blank=True, null=True)
    logframe_indicator = models.ForeignKey('indicators.Indicator', blank=True, null=True)
    non_logframe_indicator = models.CharField("Non-Logframe Indicator", max_length=255, blank=True, null=True)
    program = models.ForeignKey(Program, blank=True, null=True, related_name="q_agreement")
    community = models.ForeignKey(Community, blank=True, null=True, related_name="q_agreement")
    sector = models.ForeignKey(Sector, blank=True, null=True, related_name="q_agreement")
    agreement = models.ForeignKey(ProjectAgreement, blank=True, null=True, related_name="q_complete")
    create_date = models.DateTimeField(null=True, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ('description',)
        verbose_name_plural = "Indicator Output/Outcome Collected Data"

    #onsave add create date or update edit date
    def save(self, *args, **kwargs):
        if self.create_date == None:
            self.create_date = datetime.now()
        self.edit_date = datetime.now()
        super(CollectedData, self).save()

    #displayed in admin templates
    def __unicode__(self):
        return self.description


class CollectedDataAdmin(admin.ModelAdmin):
    list_display = ('description', 'targeted', 'achieved', 'logframe_indicator', 'non_logframe_indicator', 'create_date', 'edit_date')
    display = 'Indicator Output/Outcome Collected Data'