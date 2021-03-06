# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-06-03 05:17
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0005_treeitem_leaf'),
        ('modules', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='module',
            name='tasks',
        ),
        migrations.AddField(
            model_name='module',
            name='treeitems',
            field=models.ManyToManyField(blank=True, to='courses.TreeItem', verbose_name='Элементы дерева'),
        ),
        migrations.AlterField(
            model_name='module',
            name='comment',
            field=models.TextField(blank=True, help_text='Введите комментарий к модулю', null=True, verbose_name='Комментарий'),
        ),
        migrations.AlterField(
            model_name='module',
            name='owner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='modules', to=settings.AUTH_USER_MODEL, verbose_name='Владелец'),
        ),
    ]
