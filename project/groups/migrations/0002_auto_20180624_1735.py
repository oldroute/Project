# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-06-24 12:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='state',
            field=models.IntegerField(choices=[(0, 'Открыта'), (1, 'Закрыта'), (2, 'Кодовое слово')], default=1, verbose_name='Статус'),
        ),
        migrations.AlterField(
            model_name='group',
            name='status',
            field=models.TextField(blank=True, help_text='Введите статус группы', max_length=1024, verbose_name='Статус'),
        ),
    ]