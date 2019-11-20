# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-11-17 19:47
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='group',
            name='last_modified',
        ),
        migrations.AddField(
            model_name='group',
            name='creation_date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='дата создания'),
            preserve_default=False,
        ),
    ]