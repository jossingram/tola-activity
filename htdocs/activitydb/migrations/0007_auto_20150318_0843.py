# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('activitydb', '0006_auto_20150317_0505'),
    ]

    operations = [
        migrations.RenameField(
            model_name='quantitativeoutputs',
            old_name='project_agreement',
            new_name='agreement',
        ),
        migrations.RenameField(
            model_name='quantitativeoutputs',
            old_name='project_complete',
            new_name='complete',
        ),
    ]
