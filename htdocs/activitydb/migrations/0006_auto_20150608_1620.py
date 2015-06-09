# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('activitydb', '0005_program_sector'),
    ]

    operations = [
        migrations.CreateModel(
            name='FAQ',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('question', models.TextField(null=True, blank=True)),
                ('answer', models.TextField(null=True, blank=True)),
                ('create_date', models.DateTimeField(null=True, blank=True)),
            ],
            options={
                'ordering': ('create_date',),
            },
        ),
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('note', models.TextField()),
                ('page', models.CharField(max_length=135)),
                ('severity', models.CharField(max_length=135)),
                ('create_date', models.DateTimeField(null=True, blank=True)),
                ('submitter', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('create_date',),
            },
        ),
        migrations.AlterModelOptions(
            name='documentation',
            options={'ordering': ('create_date',)},
        ),
        migrations.RemoveField(
            model_name='documentation',
            name='description',
        ),
        migrations.RemoveField(
            model_name='documentation',
            name='edit_date',
        ),
        migrations.RemoveField(
            model_name='documentation',
            name='file_field',
        ),
        migrations.RemoveField(
            model_name='documentation',
            name='project',
        ),
        migrations.RemoveField(
            model_name='documentation',
            name='template',
        ),
        migrations.RemoveField(
            model_name='documentation',
            name='url',
        ),
        migrations.AddField(
            model_name='documentation',
            name='documentation',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='documentation',
            name='name',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
    ]
