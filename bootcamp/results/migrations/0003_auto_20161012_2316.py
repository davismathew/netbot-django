# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-10-12 23:16
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('results', '0002_result_task'),
    ]

    operations = [
        migrations.AlterField(
            model_name='result',
            name='inventory',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='inventories.Inventory'),
        ),
    ]
