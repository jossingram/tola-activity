# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('activitydb', '0023_auto_20151022_0500'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='projectagreement',
            name='stakeholder',
        ),
        migrations.AddField(
            model_name='projectagreement',
            name='stakeholder',
            field=models.ManyToManyField(to='activitydb.Stakeholder', null=True, blank=True),
        ),
    ]
