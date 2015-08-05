# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('normal', '0005_auto_20150804_0057'),
    ]

    operations = [
        migrations.AddField(
            model_name='lookup',
            name='out_raw',
            field=models.TextField(null=True, blank=True),
        ),
    ]
