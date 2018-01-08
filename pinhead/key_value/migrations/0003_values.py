# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-12-06 02:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('key_value', '0002_auto_20171205_1804'),
    ]

    operations = [
        migrations.CreateModel(
            name='Values',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('boolean_value', models.BooleanField(default=True)),
                ('char_value', models.CharField(max_length=32)),
                ('datetime_create_value', models.DateTimeField(auto_now_add=True)),
                ('datetime_update_value', models.DateTimeField(auto_now=True)),
                ('email_value', models.EmailField(max_length=254)),
                ('file_value', models.FileField(upload_to='key_value/')),
            ],
        ),
    ]