# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-10-05 12:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0003_task_network'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='credential',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='task',
            name='factfile',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
