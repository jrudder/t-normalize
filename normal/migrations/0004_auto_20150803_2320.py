# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('normal', '0003_auto_20150803_2220'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lookup',
            name='out_city',
            field=models.CharField(blank=True, null=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='lookup',
            name='out_country',
            field=models.CharField(blank=True, null=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='lookup',
            name='out_lines',
            field=models.CharField(blank=True, null=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='lookup',
            name='out_postalCode',
            field=models.CharField(blank=True, null=True, max_length=10),
        ),
        migrations.AlterField(
            model_name='lookup',
            name='out_state',
            field=models.CharField(blank=True, null=True, max_length=255),
        ),
    ]
