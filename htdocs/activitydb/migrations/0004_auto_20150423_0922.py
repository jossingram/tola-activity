# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('activitydb', '0003_auto_20150422_1613'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projectcomplete',
            name='actual_duration',
            field=models.CharField(max_length=255, null=True, blank=True),
            preserve_default=True,
        ),
    ]
