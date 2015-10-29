# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('activitydb', '0038_auto_20151028_1839'),
    ]

    operations = [

        migrations.AlterField(
            model_name='projectagreement',
            name='expected_duration',
            field=models.CharField(default='000000', editable=False, max_length=255, blank=True, help_text='[MONTHS]/[DAYS]', null=True, verbose_name='Expected duration'),
        ),
    ]
