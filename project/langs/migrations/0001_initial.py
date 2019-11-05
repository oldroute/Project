# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-10-12 19:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    operations = [
        migrations.CreateModel(
            name='Lang',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='заголовок')),
            ],
            options={
                'verbose_name': 'язык программирования',
                'verbose_name_plural': 'языки программирования',
            },
        ),
    ]