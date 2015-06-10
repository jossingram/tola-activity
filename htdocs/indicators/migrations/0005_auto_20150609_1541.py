# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('indicators', '0004_disaggregationlabel_disaggregationvalue'),
    ]

    operations = [
        migrations.AddField(
            model_name='collecteddata',
            name='disaggregation_value',
            field=models.ForeignKey(blank=True, to='indicators.DisaggregationValue', null=True),
        ),
        migrations.AlterField(
            model_name='indicator',
            name='sector',
            field=models.ForeignKey(blank=True, to='activitydb.Sector', null=True),
        ),
    ]
