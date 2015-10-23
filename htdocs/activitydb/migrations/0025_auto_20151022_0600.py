# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('activitydb', '0024_auto_20151022_0541'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='stakeholdertype',
            options={'ordering': ('name',), 'verbose_name_plural': 'Stakeholder Types'},
        ),
        migrations.RemoveField(
            model_name='stakeholdertype',
            name='country',
        ),
    ]
