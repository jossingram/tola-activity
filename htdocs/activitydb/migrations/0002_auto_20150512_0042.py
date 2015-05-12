# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('activitydb', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='programdashboard',
            old_name='project_agreement_approved',
            new_name='project_agreement_count',
        ),
        migrations.RenameField(
            model_name='programdashboard',
            old_name='project_completion_approved',
            new_name='project_agreement_count_approved',
        ),
        migrations.RenameField(
            model_name='programdashboard',
            old_name='project_proposal_approved',
            new_name='project_completion_count',
        ),
        migrations.AddField(
            model_name='programdashboard',
            name='project_completion_count_approved',
            field=models.IntegerField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='programdashboard',
            name='project_proposal_count',
            field=models.IntegerField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='programdashboard',
            name='project_proposal_count_approved',
            field=models.IntegerField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
