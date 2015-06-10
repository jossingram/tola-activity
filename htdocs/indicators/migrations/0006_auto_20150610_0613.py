# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('indicators', '0005_auto_20150609_1541'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='collecteddata',
            name='data_type',
        ),
        migrations.RemoveField(
            model_name='collecteddata',
            name='disaggregation_value',
        ),
        migrations.AddField(
            model_name='collecteddata',
            name='disaggregation_value',
            field=models.ManyToManyField(to='indicators.DisaggregationValue', null=True, blank=True),
        ),
    ]
