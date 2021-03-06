# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-10-25 12:00
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('aarong', '0029_auto_20171024_1620'),
    ]

    operations = [
        migrations.CreateModel(
            name='Area',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('areaName', models.CharField(default='', max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Branch',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('branchName', models.CharField(default='', max_length=200)),
                ('Area', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='aarong.Area')),
                ('User', models.OneToOneField(blank=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='route',
            name='RouteLat',
        ),
        migrations.RemoveField(
            model_name='route',
            name='RouteLng',
        ),
        migrations.RemoveField(
            model_name='route',
            name='User',
        ),
        migrations.AddField(
            model_name='route',
            name='Branch',
            field=models.ForeignKey(blank=True, default=1, on_delete=django.db.models.deletion.CASCADE, to='aarong.Branch'),
            preserve_default=False,
        ),
    ]
