# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-10-12 19:24
from __future__ import unicode_literals

from django.conf import settings
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion
import tinymce.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Source',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_key', models.PositiveIntegerField(default=0, verbose_name='порядок')),
                ('show', models.BooleanField(default=False, verbose_name='отображать')),
                ('last_modified', models.DateTimeField(auto_now=True, verbose_name='дата последнего изменения')),
                ('title', models.CharField(max_length=255, verbose_name='заголовок')),
                ('slug', models.SlugField(max_length=255, unique=True, verbose_name='слаг')),
                ('content', tinymce.models.HTMLField(blank=True, default='', null=True, verbose_name='содержимое')),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='автор')),
            ],
            options={
                'verbose_name': 'источник материалов',
                'verbose_name_plural': 'источники материалов',
                'ordering': ('order_key',),
            },
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_key', models.PositiveIntegerField(default=0, verbose_name='порядок')),
                ('show', models.BooleanField(default=False, verbose_name='отображать')),
                ('last_modified', models.DateTimeField(auto_now=True, verbose_name='дата последнего изменения')),
                ('title', models.CharField(max_length=255, verbose_name='заголовок')),
                ('slug', models.SlugField(max_length=255, unique=True, verbose_name='слаг')),
                ('content', tinymce.models.HTMLField(blank=True, default='', null=True, verbose_name='содержимое')),
                ('source_raw_id', models.CharField(blank=True, max_length=255, null=True, verbose_name='id в источнике')),
                ('tests', django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=list, null=True, verbose_name='тесты')),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='автор')),
                ('source', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='tasks.Source', verbose_name='источник')),
            ],
            options={
                'verbose_name': 'задача',
                'verbose_name_plural': 'задачи',
                'ordering': ('order_key',),
            },
        ),
    ]
