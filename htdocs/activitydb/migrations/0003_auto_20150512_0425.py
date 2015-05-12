# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('activitydb', '0002_auto_20150512_0042'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProfileType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('profile', models.CharField(max_length=255, verbose_name=b'Sector Name', blank=True)),
                ('create_date', models.DateTimeField(null=True, blank=True)),
                ('edit_date', models.DateTimeField(null=True, blank=True)),
            ],
            options={
                'ordering': ('profile',),
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='community',
            name='code',
        ),
        migrations.AlterField(
            model_name='community',
            name='latitude',
            field=models.DecimalField(null=True, verbose_name=b'Latitude (Coordinates)', max_digits=25, decimal_places=14, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='community',
            name='longitude',
            field=models.DecimalField(null=True, verbose_name=b'Longitude (Coordinates)', max_digits=25, decimal_places=14, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='community',
            name='name',
            field=models.CharField(max_length=255, null=True, verbose_name=b'Profile Name', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='community',
            name='type',
            field=models.ForeignKey(blank=True, to='activitydb.ProfileType', null=True),
            preserve_default=True,
        ),
    ]
