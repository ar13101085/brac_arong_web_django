# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-10-11 22:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aarong', '0025_auto_20171012_0335'),
    ]

    operations = [
        migrations.CreateModel(
            name='NiceColor',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('code', models.CharField(max_length=10)),
            ],
        ),
    ]
