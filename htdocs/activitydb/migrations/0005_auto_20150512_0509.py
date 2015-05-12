# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('activitydb', '0004_auto_20150512_0458'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='projectcomplete',
            options={'ordering': ('create_date',), 'verbose_name_plural': 'Activity Completions'},
        ),
        migrations.AlterField(
            model_name='projectagreement',
            name='project_activity',
            field=models.CharField(help_text=b'This should come directly from the activities listed in the Logframe', max_length=255, null=True, verbose_name=b'Project Activity', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='projectagreement',
            name='project_design',
            field=models.CharField(max_length=255, null=True, verbose_name=b'Activity design for', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='projectagreement',
            name='project_name',
            field=models.CharField(help_text=b'Please be specific in your name.  Consider that your Project Name includes WHO, WHAT, WHERE, HOW', max_length=255, null=True, verbose_name=b'Activity Name', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='projectcomplete',
            name='project_name',
            field=models.CharField(max_length=255, null=True, verbose_name=b'Activity Name', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='projectproposal',
            name='project_name',
            field=models.CharField(help_text=b'Please be specific in your name.  Consider that your Activity Name includes WHO, WHAT, WHERE, HOW', max_length=255, verbose_name=b'Activity Name'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='projecttype',
            name='name',
            field=models.CharField(max_length=135, verbose_name=b'Type of Activity'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='projecttypeother',
            name='name',
            field=models.CharField(max_length=135, verbose_name=b'Type of Activity'),
            preserve_default=True,
        ),
    ]
