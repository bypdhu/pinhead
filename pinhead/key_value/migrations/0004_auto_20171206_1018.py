# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-12-06 02:18
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('key_value', '0003_values'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Values',
            new_name='Value',
        ),
    ]
