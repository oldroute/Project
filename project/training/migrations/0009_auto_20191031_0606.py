# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-10-31 06:06
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('training', '0008_auto_20191030_1116'),
    ]

    operations = [
        migrations.AddField(
            model_name='taskitem',
            name='slug',
            field=models.SlugField(default=1, max_length=255, verbose_name='слаг'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='topic',
            name='slug',
            field=models.SlugField(default=1, max_length=255, verbose_name='слаг'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='solution',
            name='status',
            field=models.CharField(choices=[('0', 'нет попыток'), ('1', 'нет прогресса'), ('2', 'есть прогресс'), ('3', 'решено')], default='0', max_length=255, verbose_name='статус'),
        ),
        migrations.AlterField(
            model_name='solution',
            name='version_list',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=list, null=True, verbose_name='список сохраненных решений'),
        ),
    ]