# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('activitydb', '0007_auto_20150318_0843'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projectagreement',
            name='approval',
            field=models.CharField(default=b'in progress', max_length=255, null=True, verbose_name=b'Status', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='projectcomplete',
            name='approval',
            field=models.CharField(default=b'in progress', max_length=255, null=True, verbose_name=b'Status', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='projectproposal',
            name='approval',
            field=models.CharField(default=b'in progress', max_length=255, null=True, verbose_name=b'Status', blank=True),
            preserve_default=True,
        ),
    ]
