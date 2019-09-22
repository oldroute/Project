# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-09-21 15:00
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0005_auto_20190921_1457'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='taskitem',
            options={'ordering': ('order_key',), 'verbose_name': 'задача', 'verbose_name_plural': 'задачи'},
        ),
        migrations.AlterField(
            model_name='task',
            name='tests',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=list, null=True, verbose_name='тесты'),
        ),
    ]
