# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('activitydb', '0005_auto_20150316_0945'),
    ]

    operations = [
        migrations.AddField(
            model_name='quantitativeoutputs',
            name='achieved',
            field=models.CharField(max_length=255, null=True, verbose_name=b'Achieved #', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='quantitativeoutputs',
            name='non_logframe_indicator',
            field=models.CharField(max_length=255, null=True, verbose_name=b'Non-Logframe Indicator', blank=True),
            preserve_default=True,
        ),
    ]
