# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2017-02-08 13:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('confcreator', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='confcreator',
            name='network',
            field=models.CharField(default=b'EMC', max_length=255, null=True),
        ),
    ]
