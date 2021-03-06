# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-05-27 13:25
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import mptt.fields
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0003_auto_20180527_1423'),
    ]

    operations = [
        migrations.AlterField(
            model_name='treeitem',
            name='about',
            field=tinymce.models.HTMLField(blank=True, default='', null=True, verbose_name='описание'),
        ),
        migrations.AlterField(
            model_name='treeitem',
            name='content',
            field=tinymce.models.HTMLField(blank=True, default='', null=True, verbose_name='содержимое'),
        ),
        migrations.AlterField(
            model_name='treeitem',
            name='last_modified',
            field=models.DateTimeField(auto_now=True, verbose_name='дата последнего изменения'),
        ),
        migrations.AlterField(
            model_name='treeitem',
            name='long_title',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='длинный заголовок'),
        ),
        migrations.AlterField(
            model_name='treeitem',
            name='parent',
            field=mptt.fields.TreeForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='courses.TreeItem', verbose_name='родительский элемент'),
        ),
        migrations.AlterField(
            model_name='treeitem',
            name='show',
            field=models.BooleanField(default=True, verbose_name='отображать'),
        ),
        migrations.AlterField(
            model_name='treeitem',
            name='slug',
            field=models.SlugField(max_length=255, verbose_name='слаг'),
        ),
        migrations.AlterField(
            model_name='treeitem',
            name='title',
            field=models.CharField(max_length=255, verbose_name='заголовок'),
        ),
    ]
