# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('activitydb', '0026_auto_20151023_0034'),
    ]

    operations = [
        migrations.AddField(
            model_name='checklistitem',
            name='global_item',
            field=models.BooleanField(default=0),
            preserve_default=False,
        ),
    ]
