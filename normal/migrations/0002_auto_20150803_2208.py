# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('normal', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Lookup',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('in_lines', models.CharField(max_length=255)),
                ('in_city', models.CharField(max_length=255)),
                ('in_state', models.CharField(max_length=255)),
                ('in_zip', models.CharField(max_length=10)),
                ('in_country', models.CharField(max_length=255)),
                ('out_lines', models.CharField(max_length=255)),
                ('out_city', models.CharField(max_length=255)),
                ('out_state', models.CharField(max_length=255)),
                ('out_zip', models.CharField(max_length=10)),
                ('out_country', models.CharField(max_length=255)),
            ],
        ),
        migrations.AlterModelOptions(
            name='address',
            options={'verbose_name_plural': 'Addresses'},
        ),
    ]
