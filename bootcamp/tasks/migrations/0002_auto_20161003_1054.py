# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-10-03 10:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='inventory',
            field=models.TextField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='task',
            name='playbook',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='task',
            name='tags',
            field=models.TextField(max_length=255, null=True),
        ),
    ]
