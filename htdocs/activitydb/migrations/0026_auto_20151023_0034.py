# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('activitydb', '0025_auto_20151022_0600'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projectagreement',
            name='stakeholder',
            field=models.ManyToManyField(to='activitydb.Stakeholder', blank=True),
        ),
    ]
