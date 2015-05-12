# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('activitydb', '0003_auto_20150512_0425'),
    ]

    operations = [
        migrations.AlterField(
            model_name='community',
            name='village',
            field=models.CharField(help_text=b'', max_length=255, null=True, verbose_name=b'Village', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='monitor',
            name='frequency',
            field=models.CharField(max_length=25, null=True, verbose_name=b'Frequency', blank=True),
            preserve_default=True,
        ),
    ]
