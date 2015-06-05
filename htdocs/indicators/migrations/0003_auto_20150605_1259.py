# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('activitydb', '0004_auto_20150605_1259'),
        ('indicators', '0002_auto_20150605_0934'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReportingPeriod',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('create_date', models.DateTimeField(null=True, blank=True)),
                ('edit_date', models.DateTimeField(null=True, blank=True)),
                ('frequency', models.ForeignKey(to='indicators.ReportingFrequency')),
            ],
        ),
        migrations.RemoveField(
            model_name='collecteddata',
            name='agreement',
        ),
        migrations.RemoveField(
            model_name='collecteddata',
            name='program',
        ),
        migrations.AddField(
            model_name='collecteddata',
            name='activity',
            field=models.ForeignKey(related_name='q_activity', blank=True, to='activitydb.ProjectAgreement', null=True),
        ),
        migrations.AddField(
            model_name='collecteddata',
            name='data_type',
            field=models.CharField(max_length=255, null=True, verbose_name=b'Type of Data (number, percent, text, yes/no)', blank=True),
        ),
        migrations.AlterField(
            model_name='collecteddata',
            name='achieved',
            field=models.CharField(max_length=255, null=True, verbose_name=b'Achieved', blank=True),
        ),
        migrations.RemoveField(
            model_name='collecteddata',
            name='community',
        ),
        migrations.AddField(
            model_name='collecteddata',
            name='community',
            field=models.ManyToManyField(related_name='q_community', to='activitydb.Community', blank=True),
        ),
        migrations.RemoveField(
            model_name='collecteddata',
            name='sector',
        ),
        migrations.AddField(
            model_name='collecteddata',
            name='sector',
            field=models.ManyToManyField(related_name='q_sector', to='activitydb.Sector', blank=True),
        ),
        migrations.AlterField(
            model_name='collecteddata',
            name='targeted',
            field=models.CharField(max_length=255, null=True, verbose_name=b'Targeted', blank=True),
        ),
        migrations.AlterField(
            model_name='indicator',
            name='lop_target',
            field=models.CharField(max_length=255, null=True, verbose_name=b'LOP Target', blank=True),
        ),
        migrations.AlterField(
            model_name='indicator',
            name='objectives',
            field=models.ManyToManyField(to='indicators.Objective', blank=True),
        ),
        migrations.AddField(
            model_name='collecteddata',
            name='reporting_period',
            field=models.ForeignKey(blank=True, to='indicators.ReportingPeriod', null=True),
        ),
    ]
