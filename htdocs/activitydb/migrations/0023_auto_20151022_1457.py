# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('activitydb', '0022_documentation_program'),
    ]

    operations = [
        migrations.CreateModel(
            name='SiteProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, null=True, verbose_name='Profile Name', blank=True)),
                ('existing_village', models.BooleanField(default='False', verbose_name='Is There an existing shura or CDC?')),
                ('existing_village_descr', models.CharField(max_length=255, null=True, verbose_name='If Yes please describe', blank=True)),
                ('community_leader', models.CharField(max_length=255, null=True, verbose_name='Community Malik/Elder Name', blank=True)),
                ('head_of_institution', models.CharField(max_length=255, null=True, verbose_name='Head of Shura/Institution', blank=True)),
                ('date_of_firstcontact', models.DateTimeField(null=True, blank=True)),
                ('contact_number', models.CharField(max_length=255, null=True, verbose_name='Contact Number', blank=True)),
                ('num_members', models.CharField(max_length=255, null=True, verbose_name='Number of Members', blank=True)),
                ('distance_district_capital', models.IntegerField(help_text='In KM', null=True, verbose_name='Distance from District Capital', blank=True)),
                ('distance_site_camp', models.IntegerField(help_text='In KM', null=True, verbose_name='Distance from Site Camp', blank=True)),
                ('distance_field_office', models.IntegerField(help_text='In KM', null=True, verbose_name='Distance from MC Field Office', blank=True)),
                ('total_num_households', models.IntegerField(null=True, verbose_name='Total # Households', blank=True)),
                ('avg_household_size', models.DecimalField(null=True, verbose_name='Average Household Size', max_digits=25, decimal_places=14, blank=True)),
                ('male_0_14', models.IntegerField(null=True, verbose_name='Male age 0-14', blank=True)),
                ('female_0_14', models.IntegerField(null=True, verbose_name='Female age 0-14', blank=True)),
                ('male_15_24', models.IntegerField(null=True, verbose_name='Male age 15-24 ', blank=True)),
                ('female_15_24', models.IntegerField(null=True, verbose_name='Female age 15-24', blank=True)),
                ('male_25_59', models.IntegerField(null=True, verbose_name='Male age 25-59', blank=True)),
                ('female_25_59', models.IntegerField(null=True, verbose_name='Female age 25-59', blank=True)),
                ('male_over_60', models.IntegerField(null=True, verbose_name='Male Over 60', blank=True)),
                ('female_over_60', models.IntegerField(null=True, verbose_name='Female Over 60', blank=True)),
                ('total_population', models.IntegerField(null=True, blank=True)),
                ('total_male', models.IntegerField(null=True, blank=True)),
                ('total_female', models.IntegerField(null=True, blank=True)),
                ('total_land', models.IntegerField(help_text='In hectares/jeribs', null=True, verbose_name='Total Land', blank=True)),
                ('total_agricultural_land', models.IntegerField(help_text='In hectares/jeribs', null=True, verbose_name='Total Agricultural Land', blank=True)),
                ('total_rainfed_land', models.IntegerField(help_text='In hectares/jeribs', null=True, verbose_name='Total Rain-fed Land', blank=True)),
                ('total_horticultural_land', models.IntegerField(help_text='In hectares/jeribs', null=True, verbose_name='Total Horticultural Land', blank=True)),
                ('total_literate_peoples', models.IntegerField(null=True, verbose_name='Total Literate People', blank=True)),
                ('literate_males', models.IntegerField(null=True, verbose_name='Number of Literate Males', blank=True)),
                ('literate_females', models.IntegerField(null=True, verbose_name='Number of Literate Females', blank=True)),
                ('literacy_rate', models.IntegerField(null=True, verbose_name='Literacy Rate (%)', blank=True)),
                ('population_owning_land', models.IntegerField(help_text='(%)', null=True, verbose_name='Population Owning Land', blank=True)),
                ('avg_landholding_size', models.IntegerField(help_text='In hectares/jeribs', null=True, verbose_name='Average Landholding Size', blank=True)),
                ('population_owning_livestock', models.IntegerField(help_text='(%)', null=True, verbose_name='Population Owning Livestock', blank=True)),
                ('animal_type', models.CharField(help_text='List Animal Types', max_length=255, null=True, verbose_name='Animal Types', blank=True)),
                ('village', models.CharField(max_length=255, null=True, verbose_name='Village', blank=True)),
                ('latitude', models.DecimalField(null=True, verbose_name='Latitude (Decimal Coordinates)', max_digits=25, decimal_places=14, blank=True)),
                ('longitude', models.DecimalField(null=True, verbose_name='Longitude (Decimal Coordinates)', max_digits=25, decimal_places=14, blank=True)),
                ('altitude', models.DecimalField(null=True, verbose_name='Altitude (in meters)', max_digits=25, decimal_places=14, blank=True)),
                ('precision', models.DecimalField(null=True, verbose_name='Precision (in meters)', max_digits=25, decimal_places=14, blank=True)),
                ('approval', models.CharField(default='in progress', max_length=255, null=True, verbose_name='Approval', blank=True)),
                ('create_date', models.DateTimeField(null=True, blank=True)),
                ('edit_date', models.DateTimeField(null=True, blank=True)),
                ('approved_by', models.ForeignKey(related_name='comm_approving', blank=True, to='activitydb.TolaUser', help_text='This is the Provincial Line Manager', null=True)),
                ('country', models.ForeignKey(to='activitydb.Country')),
                ('district', models.ForeignKey(blank=True, to='activitydb.District', null=True)),
                ('filled_by', models.ForeignKey(related_name='comm_estimate', blank=True, to='activitydb.TolaUser', help_text='This is the originator', null=True)),
                ('location_verified_by', models.ForeignKey(related_name='comm_gis', blank=True, to='activitydb.TolaUser', help_text='This should be GIS Manager', null=True)),
                ('office', models.ForeignKey(default='1', to='activitydb.Office')),
                ('province', models.ForeignKey(blank=True, to='activitydb.Province', null=True)),
                ('type', models.ForeignKey(blank=True, to='activitydb.ProfileType', null=True)),
            ],
            options={
                'ordering': ('name',),
                'verbose_name_plural': 'Communities',
            },
        ),
        migrations.CreateModel(
            name='Stakeholder',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=135, verbose_name='Type of Activity')),
                ('description', models.CharField(max_length=255)),
                ('create_date', models.DateTimeField(null=True, blank=True)),
                ('edit_date', models.DateTimeField(null=True, blank=True)),
            ],
            options={
                'ordering': ('name',),
            },
        ),
        migrations.RemoveField(
            model_name='community',
            name='approved_by',
        ),
        migrations.RemoveField(
            model_name='community',
            name='country',
        ),
        migrations.RemoveField(
            model_name='community',
            name='district',
        ),
        migrations.RemoveField(
            model_name='community',
            name='filled_by',
        ),
        migrations.RemoveField(
            model_name='community',
            name='location_verified_by',
        ),
        migrations.RemoveField(
            model_name='community',
            name='office',
        ),
        migrations.RemoveField(
            model_name='community',
            name='province',
        ),
        migrations.RemoveField(
            model_name='community',
            name='type',
        ),
        migrations.AlterField(
            model_name='beneficiary',
            name='community',
            field=models.ForeignKey(blank=True, to='activitydb.SiteProfile', null=True),
        ),
        migrations.AlterField(
            model_name='projectagreement',
            name='community',
            field=models.ManyToManyField(to='activitydb.SiteProfile', blank=True),
        ),
        migrations.AlterField(
            model_name='projectcomplete',
            name='community',
            field=models.ManyToManyField(to='activitydb.SiteProfile', blank=True),
        ),
        migrations.DeleteModel(
            name='Community',
        ),
    ]
