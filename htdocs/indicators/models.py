from django.db import models
from django.contrib import admin
from django.conf import settings
from activitydb.models import Program, Sector, SiteProfile, ProjectAgreement, ProjectComplete, Country, Office, Documentation, TolaUser
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


class StrategicObjective(models.Model):
    name = models.CharField(max_length=135, blank=True)
    country = models.ForeignKey(Country, null=True, blank=True)
    description = models.CharField(max_length=765, blank=True)
    create_date = models.DateTimeField(null=True, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ('country','name')

    def __unicode__(self):
        return self.name

    def save(self):
        if self.create_date is None:
            self.create_date = datetime.now()
        super(StrategicObjective, self).save()


class StrategicObjectiveAdmin(admin.ModelAdmin):
    list_display = ('country','name')
    search_fields = ('country','name')
    display = 'Strategic Objectives'


class Objective(models.Model):
    name = models.CharField(max_length=135, blank=True)
    program = models.ForeignKey(Program, null=True, blank=True)
    description = models.CharField(max_length=765, blank=True)
    create_date = models.DateTimeField(null=True, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ('program','name')

    def __unicode__(self):
        return self.name

    def save(self):
        if self.create_date is None:
            self.create_date = datetime.now()
        super(Objective, self).save()


class ObjectiveAdmin(admin.ModelAdmin):
    list_display = ('program','name')
    search_fields = ('name','program')
    display = 'Objectives'

class Level(models.Model):
    name = models.CharField(max_length=135, blank=True)
    description = models.CharField(max_length=765, blank=True)
    create_date = models.DateTimeField(null=True, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)

    def __unicode__(self):
        return self.name

    def save(self):
        if self.create_date is None:
            self.create_date = datetime.now()
        super(Level, self).save()

class LevelAdmin(admin.ModelAdmin):
    list_display = ('name')
    display = 'Levels'


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
    frequency = models.CharField(max_length=135, blank=True)
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
    list_display = ('frequency','create_date','edit_date')
    display = 'Reporting Frequency'


class ExternalService(models.Model):
    name = models.CharField(max_length=255, blank=True)
    url = models.CharField(max_length=765, blank=True)
    feed_url = models.CharField(max_length=765, blank=True)
    create_date = models.DateTimeField(null=True, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)

    def __unicode__(self):
        return self.name


class ExternalServiceAdmin(admin.ModelAdmin):
    list_display = ('name','url','feed_url','create_date','edit_date')
    display = 'External Indicator Data Service'


class ExternalServiceRecord(models.Model):
    external_service = models.ForeignKey(ExternalService, blank=True, null=True)
    full_url = models.CharField(max_length=765, blank=True)
    record_id = models.CharField("Unique ID",max_length=765, blank=True)
    create_date = models.DateTimeField(null=True, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)

    def __unicode__(self):
        return self.full_url


class ExternalServiceRecordAdmin(admin.ModelAdmin):
    list_display = ('external_service','full_url','record_id','create_date','edit_date')
    display = 'Exeternal Indicator Data Service'


class Indicator(models.Model):
    owner = models.ForeignKey('auth.User')
    country = models.ForeignKey(Country, blank=True)
    indicator_type = models.ManyToManyField(IndicatorType, blank=True)
    level = models.ManyToManyField(Level, blank=True)
    objectives = models.ManyToManyField(Objective, blank=True, related_name="obj_indicator")
    strategic_objectives = models.ManyToManyField(StrategicObjective, blank=True, related_name="strat_indicator")
    name = models.CharField(max_length=255, null=True, blank=True)
    number = models.CharField(max_length=255, null=True, blank=True)
    source = models.CharField(max_length=255, null=True, blank=True)
    definition = models.TextField(null=True, blank=True)
    disaggregation = models.ManyToManyField(DisaggregationType, blank=True)
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
    approved_by = models.ForeignKey(TolaUser, blank=True, null=True, related_name="approving_indicator")
    approval_submitted_by = models.ForeignKey(TolaUser, blank=True, null=True, related_name="indicator_submitted_by")
    external_service_record = models.ForeignKey(ExternalServiceRecord, verbose_name="External Service ID", blank=True, null=True)
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

    @property
    def objectives_list(self):
        return ', '.join([x.name for x in self.objectives.all()])

    @property
    def strategicobjectives_list(self):
        return ', '.join([x.name for x in self.strategic_objectives.all()])

    @property
    def programs(self):
        return ', '.join([x.name for x in self.program.all()])

    @property
    def indicator_types(self):
        return ', '.join([x.indicator_type for x in self.indicator_type.all()])

    @property
    def levels(self):
        return ', '.join([x.name for x in self.level.all()])

    @property
    def disaggregations(self):
        return ', '.join([x.disaggregation_type for x in self.disaggregation.all()])

    def __unicode__(self):
        return self.name


class IndicatorAdmin(admin.ModelAdmin):
    list_display = ('owner','indicator_types','name','sector')
    search_fields = ('sector','program')
    list_filter = ('sector','program')
    display = 'Indicators'


class CollectedData(models.Model):
    targeted = models.IntegerField("Targeted", blank=True, null=True)
    achieved = models.IntegerField("Achieved", blank=True, null=True)
    disaggregation_value = models.ManyToManyField(DisaggregationValue, blank=True)
    description = models.CharField("Remarks/comments", max_length=255, blank=True, null=True)
    indicator = models.ForeignKey(Indicator, blank=True, null=True)
    agreement = models.ForeignKey(ProjectAgreement, blank=True, null=True, related_name="q_agreement2")
    complete = models.ForeignKey(ProjectComplete, blank=True, null=True, related_name="q_complete2")
    program = models.ForeignKey(Program, blank=True, null=True, related_name="i_program")
    date_collected = models.DateTimeField(null=True, blank=True)
    comment = models.CharField("Comment/Explanation", max_length=255, blank=True, null=True)
    method = models.CharField("Method of Data Collection", max_length=255, blank=True, null=True)
    tool = models.CharField("Tool/Source Developed By", max_length=255, blank=True, null=True)
    date_of_training = models.DateTimeField("Date of Staff Training", null=True, blank=True)
    date_of_analysis = models.DateTimeField("Date of Analysis", null=True, blank=True)
    trainer_name = models.CharField("Name of Trainer", max_length=255, blank=True, null=True)
    analysis_name = models.CharField("Analysis Done By", max_length=255, blank=True, null=True)
    office = models.ForeignKey(Office, blank=True, null=True, related_name="q_office")
    evidence = models.ForeignKey(Documentation, null=True, blank=True, verbose_name="Evidence Document or Link")
    create_date = models.DateTimeField(null=True, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ('agreement','indicator','date_collected','create_date')
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

    def targeted_sum(self):
        targets=CollectedData.targeted.filter(indicator__id=self).sum('targeted')
        return targets

    def achieved_sum(self):
        achieved=CollectedData.targeted.filter(indicator__id=self).sum('achieved')
        return achieved


class CollectedDataAdmin(admin.ModelAdmin):
    list_display = ('description', 'targeted', 'achieved', 'indicator','disaggregation_value','community','sector','date_collected', 'create_date', 'edit_date')
    display = 'Indicator Output/Outcome Collected Data'
