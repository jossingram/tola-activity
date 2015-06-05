# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('activitydb', '0003_auto_20150605_0321'),
    ]

    operations = [
        migrations.AlterField(
            model_name='benchmarks',
            name='percent_complete',
            field=models.IntegerField(null=True, verbose_name=b'% complete', blank=True),
        ),
        migrations.AlterField(
            model_name='benchmarks',
            name='percent_cumulative',
            field=models.IntegerField(null=True, verbose_name=b'% cumulative completion', blank=True),
        ),
        migrations.AlterField(
            model_name='projectagreement',
            name='community',
            field=models.ManyToManyField(to='activitydb.Community', blank=True),
        ),
        migrations.AlterField(
            model_name='projectcomplete',
            name='community',
            field=models.ManyToManyField(to='activitydb.Community', blank=True),
        ),
        migrations.AlterField(
            model_name='projectproposal',
            name='community',
            field=models.ManyToManyField(to='activitydb.Community', blank=True),
        ),
    ]
