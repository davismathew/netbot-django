# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-10-13 15:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('results', '0006_auto_20161012_2331'),
    ]

    operations = [
        migrations.AddField(
            model_name='result',
            name='outputfile',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
