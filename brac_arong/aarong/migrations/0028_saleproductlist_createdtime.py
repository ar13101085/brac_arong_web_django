# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-10-24 04:30
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('aarong', '0027_auto_20171012_0704'),
    ]

    operations = [
        migrations.AddField(
            model_name='saleproductlist',
            name='CreatedTime',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
