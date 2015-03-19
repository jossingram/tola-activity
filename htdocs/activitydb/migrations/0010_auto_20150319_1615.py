# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('activitydb', '0009_auto_20150319_1605'),
    ]

    operations = [
        migrations.AddField(
            model_name='projectagreement',
            name='finance_reviewed_by',
            field=models.ForeignKey(related_name='finance_reviewing', blank=True, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='projectagreement',
            name='finance_reviewed_by_date',
            field=models.DateTimeField(null=True, verbose_name=b'Date Reviewed', blank=True),
            preserve_default=True,
        ),
    ]
