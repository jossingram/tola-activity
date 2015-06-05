# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('activitydb', '0002_auto_20150513_2329'),
    ]

    operations = [
        migrations.AlterField(
            model_name='community',
            name='existing_village',
            field=models.BooleanField(default=b'False', verbose_name=b'Is There an existing shura or CDC?'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='community',
            name='num_members',
            field=models.CharField(max_length=255, null=True, verbose_name=b'Number of Members', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='quantitativeoutputs',
            name='achieved',
            field=models.IntegerField(null=True, verbose_name=b'Achieved #', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='quantitativeoutputs',
            name='targeted',
            field=models.IntegerField(null=True, verbose_name=b'Targeted #', blank=True),
            preserve_default=True,
        ),
    ]
