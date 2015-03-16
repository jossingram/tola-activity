# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('activitydb', '0002_auto_20150314_1104'),
    ]

    operations = [
        migrations.AddField(
            model_name='projectcomplete',
            name='actual_duration',
            field=models.DateTimeField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='projectcomplete',
            name='expected_duration',
            field=models.CharField(help_text=b'Comes from Form-04 Project Agreement', max_length=255, null=True, verbose_name=b'Expected Duration', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='projectcomplete',
            name='actual_budget',
            field=models.CharField(help_text=b'What was the actual final cost?  This should match any financial documentation you have in the file.   It should be completely documented and verifiable by finance and any potential audit', max_length=255, null=True, verbose_name=b'Actual Budget', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='projectcomplete',
            name='actual_start_date',
            field=models.DateTimeField(help_text=b'Comes from Form-04 Project Agreement', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='projectcomplete',
            name='estimated_budget',
            field=models.CharField(help_text=b'Comes from Form-04 Project Agreement', max_length=255, null=True, verbose_name=b'Estimated Budget', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='projectcomplete',
            name='expected_end_date',
            field=models.DateTimeField(help_text=b'Comes from Form-04 Project Agreement', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='projectcomplete',
            name='expected_start_date',
            field=models.DateTimeField(help_text=b'Comes from Form-04 Project Agreement', null=True, blank=True),
            preserve_default=True,
        ),
    ]
