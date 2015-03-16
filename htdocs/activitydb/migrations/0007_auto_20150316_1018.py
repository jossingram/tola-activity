# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('activitydb', '0006_auto_20150316_1017'),
    ]

    operations = [
        migrations.AlterField(
            model_name='beneficiary',
            name='training',
            field=models.ForeignKey(blank=True, to='activitydb.TrainingAttendance', null=True),
            preserve_default=True,
        ),
    ]
