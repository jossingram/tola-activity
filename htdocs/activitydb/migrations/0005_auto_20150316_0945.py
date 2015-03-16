# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('activitydb', '0004_auto_20150316_0541'),
    ]

    operations = [
        migrations.AddField(
            model_name='community',
            name='office',
            field=models.ForeignKey(default=b'1', to='activitydb.Office'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='community',
            name='avg_household_size',
            field=models.IntegerField(help_text=b'', null=True, verbose_name=b'Average Household Size', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='community',
            name='female_0_14',
            field=models.IntegerField(null=True, verbose_name=b'Female age 0-14', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='community',
            name='female_15_24',
            field=models.IntegerField(null=True, verbose_name=b'Female age 15-24', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='community',
            name='female_25_59',
            field=models.IntegerField(null=True, verbose_name=b'Female age 25-59', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='community',
            name='female_over_60',
            field=models.IntegerField(null=True, verbose_name=b'Female Over 60', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='community',
            name='male_0_14',
            field=models.IntegerField(null=True, verbose_name=b'Male age 0-14', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='community',
            name='male_15_24',
            field=models.IntegerField(null=True, verbose_name=b'Male age 15-24 ', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='community',
            name='male_25_59',
            field=models.IntegerField(null=True, verbose_name=b'Male age 25-59', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='community',
            name='male_over_60',
            field=models.IntegerField(null=True, verbose_name=b'Male Over 60', blank=True),
            preserve_default=True,
        ),
    ]
