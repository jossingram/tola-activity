# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('activitydb', '0045_remove_siteprofile_head_of_institution'),
    ]

    operations = [
        migrations.AlterField(
            model_name='siteprofile',
            name='households_owning_livestock',
            field=models.IntegerField(help_text='(%)', null=True, verbose_name='Households Owning Livestock', blank=True),
        ),
    ]
