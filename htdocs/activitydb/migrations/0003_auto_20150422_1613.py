# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('activitydb', '0002_auto_20150409_1445'),
    ]

    operations = [
        migrations.AddField(
            model_name='budget',
            name='complete',
            field=models.ForeignKey(blank=True, to='activitydb.ProjectComplete', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='quantitativeoutputs',
            name='description',
            field=models.CharField(max_length=255, null=True, verbose_name=b'Description', blank=True),
            preserve_default=True,
        ),
    ]
