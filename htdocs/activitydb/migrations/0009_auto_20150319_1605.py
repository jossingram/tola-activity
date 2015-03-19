# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('activitydb', '0008_auto_20150318_1433'),
    ]

    operations = [
        migrations.AddField(
            model_name='projectagreement',
            name='approved_by_date',
            field=models.DateTimeField(null=True, verbose_name=b'Date Approved', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='projectagreement',
            name='checked_by_date',
            field=models.DateTimeField(null=True, verbose_name=b'Date Checked', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='projectagreement',
            name='estimated_by_date',
            field=models.DateTimeField(null=True, verbose_name=b'Date Estimated', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='projectagreement',
            name='me_reviewed_by',
            field=models.ForeignKey(related_name='reviewing_me', blank=True, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='projectagreement',
            name='me_reviewed_by_date',
            field=models.DateTimeField(null=True, verbose_name=b'Date Reviewed by M&E', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='projectagreement',
            name='reviewed_by_date',
            field=models.DateTimeField(null=True, verbose_name=b'Date Reviewed', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='trainingattendance',
            name='create_date',
            field=models.DateTimeField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='trainingattendance',
            name='edit_date',
            field=models.DateTimeField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
