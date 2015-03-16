# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('activitydb', '0005_auto_20150316_0945'),
    ]

    operations = [
        migrations.AddField(
            model_name='trainingattendance',
            name='create_date',
            field=models.DateTimeField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='trainingattendance',
            name='edit_date',
            field=models.DateTimeField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='beneficiary',
            name='training',
            field=models.ManyToManyField(to='activitydb.TrainingAttendance', null=True, blank=True),
            preserve_default=True,
        ),
    ]
