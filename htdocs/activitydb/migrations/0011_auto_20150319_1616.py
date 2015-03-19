# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('activitydb', '0010_auto_20150319_1615'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projectagreement',
            name='finance_reviewed_by_date',
            field=models.DateTimeField(null=True, verbose_name=b'Date Reviewed by Finance', blank=True),
            preserve_default=True,
        ),
    ]
