# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('activitydb', '0007_auto_20150513_2202'),
    ]

    operations = [
        migrations.AddField(
            model_name='program',
            name='sector',
            field=models.ForeignKey(blank=True, to='activitydb.Sector', null=True),
            preserve_default=True,
        ),
    ]
