# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-12-01 08:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MyCron_Job',
            fields=[
                ('id', models.CharField(max_length=128, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('cron_expr', models.CharField(max_length=128)),
                ('status', models.IntegerField(default=0)),
                ('start_time', models.DateTimeField(verbose_name='start time')),
                ('last_run_time', models.DateTimeField(verbose_name='last run time')),
                ('next_run_time', models.DateTimeField(verbose_name='next run time')),
            ],
        ),
    ]