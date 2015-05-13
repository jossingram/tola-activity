# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('activitydb', '0005_auto_20150512_0509'),
    ]

    operations = [
        migrations.RenameField(
            model_name='quantitativeoutputs',
            old_name='logframe_indicator',
            new_name='indicator',
        ),
        migrations.RemoveField(
            model_name='quantitativeoutputs',
            name='non_logframe_indicator',
        ),
    ]
