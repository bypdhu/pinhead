# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-12-05 09:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mycronjob', '0003_auto_20171201_1727'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='description',
            field=models.CharField(blank=True, default='', max_length=512),
        ),
        migrations.AlterField(
            model_name='job',
            name='last_run_time',
            field=models.DateTimeField(blank=True, verbose_name='last run time'),
        ),
        migrations.AlterField(
            model_name='job',
            name='next_run_time',
            field=models.DateTimeField(blank=True, verbose_name='next run time'),
        ),
        migrations.AlterField(
            model_name='job',
            name='start_time',
            field=models.DateTimeField(blank=True, verbose_name='start time'),
        ),
        migrations.AlterField(
            model_name='job',
            name='status',
            field=models.IntegerField(blank=True, default=0),
        ),
    ]
