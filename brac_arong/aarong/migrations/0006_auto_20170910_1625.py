# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-09-10 10:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aarong', '0005_category_categoryphoto'),
    ]

    operations = [
        migrations.RenameField(
            model_name='shop',
            old_name='ShopAddress',
            new_name='ShopDetailsAddress',
        ),
        migrations.AddField(
            model_name='shop',
            name='ShopGpsAddress',
            field=models.CharField(default='', max_length=200),
        ),
    ]