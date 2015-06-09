# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('activitydb', '0006_auto_20150608_1620'),
    ]

    operations = [
        migrations.CreateModel(
            name='DocumentationApp',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, null=True, blank=True)),
                ('documentation', models.TextField(null=True, blank=True)),
                ('create_date', models.DateTimeField(null=True, blank=True)),
            ],
            options={
                'ordering': ('create_date',),
            },
        ),
        migrations.AlterModelOptions(
            name='documentation',
            options={'ordering': ('name',), 'verbose_name_plural': 'Documentation'},
        ),
        migrations.RemoveField(
            model_name='documentation',
            name='documentation',
        ),
        migrations.AddField(
            model_name='documentation',
            name='description',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='documentation',
            name='edit_date',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='documentation',
            name='file_field',
            field=models.FileField(null=True, upload_to=b'uploads', blank=True),
        ),
        migrations.AddField(
            model_name='documentation',
            name='project',
            field=models.ForeignKey(blank=True, to='activitydb.ProjectProposal', null=True),
        ),
        migrations.AddField(
            model_name='documentation',
            name='template',
            field=models.ForeignKey(blank=True, to='activitydb.Template', null=True),
        ),
        migrations.AddField(
            model_name='documentation',
            name='url',
            field=models.CharField(max_length=135, null=True, verbose_name=b'URL (Link to document or document repository)', blank=True),
        ),
        migrations.AlterField(
            model_name='documentation',
            name='name',
            field=models.CharField(max_length=135, null=True, verbose_name=b'Name of Document', blank=True),
        ),
    ]
