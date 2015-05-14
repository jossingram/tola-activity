# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('activitydb', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='program',
            name='sector',
            field=models.ForeignKey(blank=True, to='activitydb.Sector', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='community',
            name='avg_household_size',
            field=models.DecimalField(null=True, verbose_name=b'Average Household Size', max_digits=25, decimal_places=14, blank=True),
            preserve_default=True,
        ),
    ]
