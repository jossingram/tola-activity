# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('indicators', '0001_initial'),
        ('activitydb', '0004_auto_20150423_0922'),
    ]

    operations = [
        migrations.AddField(
            model_name='quantitativeoutputs',
            name='logframe_indicator',
            field=models.ForeignKey(blank=True, to='indicators.Indicator', null=True),
            preserve_default=True,
        ),
    ]
