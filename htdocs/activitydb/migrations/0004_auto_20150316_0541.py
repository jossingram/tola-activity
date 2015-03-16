# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('activitydb', '0003_auto_20150315_1841'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='community',
            name='community_mobilizer',
        ),
        migrations.RemoveField(
            model_name='community',
            name='community_rep',
        ),
        migrations.RemoveField(
            model_name='community',
            name='community_rep_contact',
        ),
        migrations.AddField(
            model_name='community',
            name='animal_type',
            field=models.CharField(help_text=b'See Guide for Calculation', max_length=255, null=True, verbose_name=b'Animal Types', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='community',
            name='approval',
            field=models.CharField(default=b'in progress', max_length=255, null=True, verbose_name=b'Approval', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='community',
            name='approved_by',
            field=models.ForeignKey(related_name='comm_approving', blank=True, to=settings.AUTH_USER_MODEL, help_text=b'This is the Provincial Line Manager', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='community',
            name='avg_household_size',
            field=models.IntegerField(help_text=b'In KM', null=True, verbose_name=b'Average Household Size', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='community',
            name='avg_landholding_size',
            field=models.IntegerField(help_text=b'In hectares/jeribs', null=True, verbose_name=b'Average Landholding Size', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='community',
            name='community_leader',
            field=models.CharField(max_length=255, null=True, verbose_name=b'Community Malik/Elder Name', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='community',
            name='contact_number',
            field=models.CharField(max_length=255, null=True, verbose_name=b'Head of Shura/Institution', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='community',
            name='date_of_firstcontact',
            field=models.DateTimeField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='community',
            name='distance_district_capital',
            field=models.IntegerField(help_text=b'In KM', null=True, verbose_name=b'Distance from District Capital', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='community',
            name='distance_field_office',
            field=models.IntegerField(help_text=b'In KM', null=True, verbose_name=b'Distance from MC Field Office', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='community',
            name='distance_site_camp',
            field=models.IntegerField(help_text=b'In KM', null=True, verbose_name=b'Distance from Site Camp', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='community',
            name='existing_village',
            field=models.BooleanField(default=b'True', verbose_name=b'Is There an existing shura or CDC?'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='community',
            name='existing_village_descr',
            field=models.CharField(max_length=255, null=True, verbose_name=b'If Yes please describe', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='community',
            name='female_0_14',
            field=models.IntegerField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='community',
            name='female_15_24',
            field=models.IntegerField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='community',
            name='female_25_59',
            field=models.IntegerField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='community',
            name='female_over_60',
            field=models.IntegerField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='community',
            name='filled_by',
            field=models.ForeignKey(related_name='comm_estimate', blank=True, to=settings.AUTH_USER_MODEL, help_text=b'This is the originator', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='community',
            name='head_of_institution',
            field=models.CharField(max_length=255, null=True, verbose_name=b'Head of Shura/Institution', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='community',
            name='literacy_rate',
            field=models.IntegerField(help_text=b'', null=True, verbose_name=b'Literacy Rate (%)', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='community',
            name='literate_females',
            field=models.IntegerField(help_text=b'', null=True, verbose_name=b'Number of Literate Females', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='community',
            name='literate_males',
            field=models.IntegerField(help_text=b'', null=True, verbose_name=b'Number of Literate Males', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='community',
            name='male_0_14',
            field=models.IntegerField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='community',
            name='male_15_24',
            field=models.IntegerField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='community',
            name='male_25_59',
            field=models.IntegerField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='community',
            name='male_over_60',
            field=models.IntegerField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='community',
            name='num_animals_population_owning',
            field=models.CharField(help_text=b'What?', max_length=255, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='community',
            name='num_members',
            field=models.CharField(max_length=255, null=True, verbose_name=b'Number of Memebers', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='community',
            name='population_owning_land',
            field=models.IntegerField(help_text=b'(%)', null=True, verbose_name=b'Population Owning Land', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='community',
            name='population_owning_livestock',
            field=models.IntegerField(help_text=b'(%)', null=True, verbose_name=b'Population Owning Livestock', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='community',
            name='total_agricultural_land',
            field=models.IntegerField(help_text=b'In hectares/jeribs', null=True, verbose_name=b'Total Agricultural Land', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='community',
            name='total_horticultural_land',
            field=models.IntegerField(help_text=b'In hectares/jeribs', null=True, verbose_name=b'Total Horticultural Land', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='community',
            name='total_land',
            field=models.IntegerField(help_text=b'In hectares/jeribs', null=True, verbose_name=b'Total Land', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='community',
            name='total_literate_peoples',
            field=models.IntegerField(help_text=b'', null=True, verbose_name=b'Total Literate People', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='community',
            name='total_num_households',
            field=models.IntegerField(help_text=b'', null=True, verbose_name=b'Total # Households', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='community',
            name='total_population',
            field=models.IntegerField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='community',
            name='total_rainfed_land',
            field=models.IntegerField(help_text=b'In hectares/jeribs', null=True, verbose_name=b'Total Rain-fed Land', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='community',
            name='type',
            field=models.CharField(max_length=255, null=True, verbose_name=b'Profile Type', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='community',
            name='code',
            field=models.CharField(help_text=b'See AIMS Village (Shura) Code', max_length=255, null=True, verbose_name=b'Community Profile Code', blank=True),
            preserve_default=True,
        ),
    ]
