# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-21 05:44
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('aarong', '0009_auto_20170921_1046'),
    ]

    operations = [
        migrations.AlterField(
            model_name='saleproductlist',
            name='Product',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='aarong.Product'),
        ),
    ]
