# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('activitydb', '0039_auto_20151028_1848'),
    ]

    operations = [

        migrations.AlterField(
            model_name='projectagreement',
            name='expected_duration',
            field=models.CharField(help_text='[MONTHS]/[DAYS]', max_length=255, null=True, verbose_name='Expected duration', blank=True),
        ),
    ]
