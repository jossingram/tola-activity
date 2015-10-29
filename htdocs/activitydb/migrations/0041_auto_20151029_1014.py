# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('activitydb', '0040_auto_20151028_1900'),
    ]

    operations = [
         migrations.AlterField(
            model_name='siteprofile',
            name='contact_leader',
            field=models.CharField(max_length=255, null=True, verbose_name='Contact Name', blank=True),
        ),
    ]
