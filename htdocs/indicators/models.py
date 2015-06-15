from django.db import models
from django.contrib import admin
from django.conf import settings
from activitydb.models import Program, Sector, Community, ProjectAgreement
from datetime import datetime


class IndicatorType(models.Model):
    indicator_type = models.CharField(max_length=135, blank=True)
    description = models.CharField(max_length=765, blank=True)
    create_date = models.DateTimeField(null=True, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)

    def __unicode__(self):
        return self.indicator_type


class Objective(models.Model):
    name = models.CharField(max_length=135, blank=True)
    description = models.CharField(max_length=765, blank=True)
    create_date = models.DateTimeField(null=True, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)

    def __unicode__(self):
        return self.name


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


class DisaggregationLabel(models.Model):
    disaggregation_type = models.ForeignKey(DisaggregationType)
    label = models.CharField(max_length=765, blank=True)
    create_date = models.DateTimeField(null=True, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)

    def __unicode__(self):
        return self.label


class DisaggregationLabelAdmin(admin.ModelAdmin):
    list_display = ('disaggregation_type','label','create_date','edit_date')
    display = 'Disaggregation Label'


class DisaggregationValue(models.Model):
    disaggregation_label = models.ForeignKey(DisaggregationLabel)
    value = models.CharField(max_length=765, blank=True)
    create_date = models.DateTimeField(null=True, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)

    def __unicode__(self):
        return self.value


class DisaggregationValueAdmin(admin.ModelAdmin):
    list_display = ('disaggregation_label','value','create_date','edit_date')
    display = 'Disaggregation Value'


class ReportingFrequency(models.Model):
    frequency= models.CharField(max_length=135, blank=True)
    description = models.CharField(max_length=765, blank=True)
    create_date = models.DateTimeField(null=True, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)

    def __unicode__(self):
        return self.frequency


class ReportingFrequencyAdmin(admin.ModelAdmin):
    list_display = ('frequency','description','create_date','edit_date')
    display = 'Reporting Frequency'


class ReportingPeriod(models.Model):
    frequency = models.ForeignKey(ReportingFrequency)
    create_date = models.DateTimeField(null=True, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)

    def __unicode__(self):
        return self.frequency


class ReportingPeriodAdmin(admin.ModelAdmin):
    list_display = ('frequency','description','create_date','edit_date')
    display = 'Reporting Frequency'


class Indicator(models.Model):
    owner = models.ForeignKey('auth.User')
    indicator_type = models.ForeignKey(IndicatorType, null=True, blank=True)
    objectives = models.ManyToManyField(Objective, blank=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    number = models.CharField(max_length=255, null=True, blank=True)
    source = models.CharField(max_length=255, null=True, blank=True)
    definition = models.CharField(max_length=255, null=True, blank=True)
    disaggregation = models.ForeignKey(DisaggregationType, null=True, blank=True)
    baseline = models.CharField(max_length=255, null=True, blank=True)
    lop_target = models.CharField("LOP Target",max_length=255, null=True, blank=True)
    means_of_verification = models.CharField(max_length=255, null=True, blank=True)
    data_collection_method = models.CharField(max_length=255, null=True, blank=True)
    responsible_person = models.CharField(max_length=255, null=True, blank=True)
    method_of_analysis = models.CharField(max_length=255, null=True, blank=True)
    information_use = models.CharField(max_length=255, null=True, blank=True)
    reporting_frequency = models.ForeignKey(ReportingFrequency, null=True, blank=True)
    comments = models.CharField(max_length=255, null=True, blank=True)
    program = models.ManyToManyField(Program)
    sector = models.ForeignKey(Sector, null=True, blank=True)
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

    def program_str(self):
        return ', '.join([program.name for program in value.all()])

    def __unicode__(self):
        return self.name


class IndicatorAdmin(admin.ModelAdmin):
    list_display = ('owner','indicator_type','name','sector','description', 'program')
    display = 'Indicators'


class CollectedData(models.Model):
    targeted = models.CharField("Targeted", max_length=255, blank=True, null=True)
    achieved = models.CharField("Achieved", max_length=255, blank=True, null=True)
    disaggregation_value = models.ManyToManyField(DisaggregationValue, blank=True)
    description = models.CharField("Description", max_length=255, blank=True, null=True)
    indicator = models.ForeignKey(Indicator, blank=True, null=True)
    community = models.ManyToManyField(Community, blank=True, related_name="q_community")
    sector = models.ManyToManyField(Sector, blank=True, related_name="q_sector")
    date_collected = models.DateTimeField(null=True, blank=True)
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
    list_display = ('description', 'targeted', 'achieved', 'indicator','disaggregation_value','community','sector','date_collected', 'create_date', 'edit_date')
    display = 'Indicator Output/Outcome Collected Data'
