# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-10 18:36
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pic', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='photo',
            name='title',
        ),
    ]
