# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.CharField(max_length=64, primary_key=True, serialize=False)),
                ('lines', models.CharField(max_length=200)),
                ('city', models.CharField(max_length=64)),
                ('state', models.CharField(max_length=2)),
                ('postalCode', models.CharField(max_length=5)),
            ],
        ),
        migrations.CreateModel(
            name='AddressNormal',
            fields=[
                ('id', models.CharField(max_length=64, primary_key=True, serialize=False)),
                ('lines', models.CharField(max_length=200)),
                ('city', models.CharField(max_length=64)),
                ('state', models.CharField(max_length=2)),
                ('postalCode', models.CharField(max_length=5)),
            ],
        ),
        migrations.AddField(
            model_name='address',
            name='normal',
            field=models.ForeignKey(to='normal.AddressNormal'),
        ),
    ]
