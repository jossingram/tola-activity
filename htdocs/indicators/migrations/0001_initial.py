# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('activitydb', '0004_auto_20150423_0922'),
    ]

    operations = [
        migrations.CreateModel(
            name='DisaggregationType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('disaggregation_type', models.CharField(max_length=135, blank=True)),
                ('description', models.CharField(max_length=765, blank=True)),
                ('create_date', models.DateTimeField(null=True, blank=True)),
                ('edit_date', models.DateTimeField(null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Indicator',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, null=True, blank=True)),
                ('number', models.CharField(max_length=255, null=True, blank=True)),
                ('source', models.CharField(max_length=255, null=True, blank=True)),
                ('definition', models.CharField(max_length=255, null=True, blank=True)),
                ('baseline', models.CharField(max_length=255, null=True, blank=True)),
                ('lop_target', models.CharField(max_length=255, null=True, blank=True)),
                ('means_of_verification', models.CharField(max_length=255, null=True, blank=True)),
                ('data_collection_method', models.CharField(max_length=255, null=True, blank=True)),
                ('responsible_person', models.CharField(max_length=255, null=True, blank=True)),
                ('method_of_analysis', models.CharField(max_length=255, null=True, blank=True)),
                ('information_use', models.CharField(max_length=255, null=True, blank=True)),
                ('comments', models.CharField(max_length=255, null=True, blank=True)),
                ('create_date', models.DateTimeField(null=True, blank=True)),
                ('edit_date', models.DateTimeField(null=True, blank=True)),
                ('approval_submitted_by', models.ForeignKey(related_name='indicator_submitted_by', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('approved_by', models.ForeignKey(related_name='approving_indicator', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('disaggregation', models.ForeignKey(blank=True, to='indicators.DisaggregationType', null=True)),
            ],
            options={
                'ordering': ('create_date',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='IndicatorType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('indicator_type', models.CharField(max_length=135, blank=True)),
                ('description', models.CharField(max_length=765, blank=True)),
                ('create_date', models.DateTimeField(null=True, blank=True)),
                ('edit_date', models.DateTimeField(null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ReportingFrequency',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('frequency', models.CharField(max_length=135, blank=True)),
                ('description', models.CharField(max_length=765, blank=True)),
                ('create_date', models.DateTimeField(null=True, blank=True)),
                ('edit_date', models.DateTimeField(null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='indicator',
            name='indicator_type',
            field=models.ForeignKey(blank=True, to='indicators.IndicatorType', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='indicator',
            name='owner',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='indicator',
            name='program',
            field=models.ManyToManyField(to='activitydb.Program'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='indicator',
            name='reporting_frequency',
            field=models.ForeignKey(blank=True, to='indicators.ReportingFrequency', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='indicator',
            name='sector',
            field=models.ForeignKey(to='activitydb.Sector'),
            preserve_default=True,
        ),
    ]
