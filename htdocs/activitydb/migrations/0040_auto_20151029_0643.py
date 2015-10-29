# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('activitydb', '0039_auto_20151029_0628'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='siteprofile',
            name='households_owning_land',
        ),
        migrations.AddField(
            model_name='siteprofile',
            name='populations_owning_land',
            field=models.IntegerField(help_text='(%)', null=True, verbose_name='Households Owning Land', blank=True),
        ),
    ]
