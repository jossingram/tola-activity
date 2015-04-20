# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('indicators', '0001_initial'),
    ]

    operations = [
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
        migrations.AlterField(
            model_name='indicator',
            name='indicator_type',
            field=models.ForeignKey(blank=True, to='indicators.IndicatorType', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='indicator',
            name='name',
            field=models.CharField(max_length=255, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='indicator',
            name='reporting_frequency',
            field=models.ForeignKey(blank=True, to='indicators.ReportingFrequency', null=True),
            preserve_default=True,
        ),
    ]
