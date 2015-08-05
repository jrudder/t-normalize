# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('normal', '0004_auto_20150803_2320'),
    ]

    operations = [
        migrations.RenameField(
            model_name='lookup',
            old_name='in_lines',
            new_name='in_line1',
        ),
        migrations.RenameField(
            model_name='lookup',
            old_name='out_lines',
            new_name='in_line2',
        ),
        migrations.AddField(
            model_name='lookup',
            name='out_line1',
            field=models.CharField(blank=True, null=True, max_length=255),
        ),
        migrations.AddField(
            model_name='lookup',
            name='out_line2',
            field=models.CharField(blank=True, null=True, max_length=255),
        ),
    ]
