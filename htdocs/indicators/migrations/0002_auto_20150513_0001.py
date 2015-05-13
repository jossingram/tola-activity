# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('indicators', '0001_initial'),
        ('activitydb', '0001_initial'),  # Add this line
    ]

    operations = [
        migrations.CreateModel(
            name='CollectedData',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('targeted', models.CharField(max_length=255, null=True, verbose_name=b'Targeted #', blank=True)),
                ('achieved', models.CharField(max_length=255, null=True, verbose_name=b'Achieved #', blank=True)),
                ('description', models.CharField(max_length=255, null=True, verbose_name=b'Description', blank=True)),
                ('create_date', models.DateTimeField(null=True, blank=True)),
                ('edit_date', models.DateTimeField(null=True, blank=True)),
                ('agreement', models.ForeignKey(related_name='q_complete', blank=True, to='activitydb.ProjectAgreement', null=True)),
                ('community', models.ForeignKey(related_name='q_agreement', blank=True, to='activitydb.Community', null=True)),
            ],
            options={
                'ordering': ('description',),
                'verbose_name_plural': 'Indicator Output/Outcome Collected Data',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='collecteddata',
            name='indicator',
            field=models.ForeignKey(blank=True, to='indicators.Indicator', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='collecteddata',
            name='program',
            field=models.ForeignKey(related_name='q_agreement', blank=True, to='activitydb.Program', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='collecteddata',
            name='sector',
            field=models.ForeignKey(related_name='q_agreement', blank=True, to='activitydb.Sector', null=True),
            preserve_default=True,
        ),
    ]
