# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('activitydb', '0004_auto_20150605_1259'),
    ]

    operations = [
        migrations.AddField(
            model_name='program',
            name='sector',
            field=models.ForeignKey(blank=True, to='activitydb.Sector', null=True),
        ),
    ]
