# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('indicators', '0003_auto_20150605_1259'),
    ]

    operations = [
        migrations.CreateModel(
            name='DisaggregationLabel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('label', models.CharField(max_length=765, blank=True)),
                ('create_date', models.DateTimeField(null=True, blank=True)),
                ('edit_date', models.DateTimeField(null=True, blank=True)),
                ('disaggregation_type', models.ForeignKey(to='indicators.DisaggregationType')),
            ],
        ),
        migrations.CreateModel(
            name='DisaggregationValue',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('value', models.CharField(max_length=765, blank=True)),
                ('create_date', models.DateTimeField(null=True, blank=True)),
                ('edit_date', models.DateTimeField(null=True, blank=True)),
                ('disaggregation_label', models.ForeignKey(to='indicators.DisaggregationLabel')),
            ],
        ),
    ]
