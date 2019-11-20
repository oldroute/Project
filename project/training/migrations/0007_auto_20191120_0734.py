# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-11-20 07:34
from __future__ import unicode_literals

from django.db import migrations
import project.training.fields


class Migration(migrations.Migration):

    dependencies = [
        ('training', '0006_auto_20191120_0726'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='order_key',
            field=project.training.fields.OrderField(blank=True, null=True, verbose_name='порядок'),
        ),
        migrations.AlterField(
            model_name='taskitem',
            name='order_key',
            field=project.training.fields.OrderField(blank=True, null=True, verbose_name='порядок'),
        ),
        migrations.AlterField(
            model_name='topic',
            name='order_key',
            field=project.training.fields.OrderField(blank=True, null=True, verbose_name='порядок'),
        ),
    ]
