# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('activitydb', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projectagreement',
            name='capacity',
            field=models.CharField(max_length=255, null=True, verbose_name=b'Capacity', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='projectagreement',
            name='evaluate',
            field=models.CharField(max_length=255, null=True, verbose_name=b'How will you evaluate the outcome or impact of the project?', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='quantitativeoutputs',
            name='project_complete',
            field=models.ForeignKey(related_name='q_complete', blank=True, to='activitydb.ProjectComplete', null=True),
            preserve_default=True,
        ),
    ]
