# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('normal', '0002_auto_20150803_2208'),
    ]

    operations = [
        migrations.RenameField(
            model_name='lookup',
            old_name='in_zip',
            new_name='in_postalCode',
        ),
        migrations.RenameField(
            model_name='lookup',
            old_name='out_zip',
            new_name='out_postalCode',
        ),
        migrations.AddField(
            model_name='lookup',
            name='provider',
            field=models.CharField(max_length=32, default='local'),
            preserve_default=False,
        ),
    ]
