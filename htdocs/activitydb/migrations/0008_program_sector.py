# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('activitydb', '0007_auto_20150513_2202'),
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
        migrations.AlterField(
            model_name='profiletype',
            name='profile',
            field=models.CharField(max_length=255, verbose_name=b'Profile Name', blank=True),
            preserve_default=True,
        ),
    ]
