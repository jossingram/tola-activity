# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('indicators', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Objective',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=135, blank=True)),
                ('description', models.CharField(max_length=765, blank=True)),
                ('create_date', models.DateTimeField(null=True, blank=True)),
                ('edit_date', models.DateTimeField(null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='indicator',
            name='objectives',
            field=models.ManyToManyField(to='indicators.Objective', null=True, blank=True),
            preserve_default=True,
        ),
    ]
