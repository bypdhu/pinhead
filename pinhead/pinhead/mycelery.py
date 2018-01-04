#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Author  : bianbian
# @Site    : Asia/Shanghai
# @File    : celery.py
# @Software: bianbian's PyCharm
# @Time    : 2018/1/3 17:54

import os
from celery import Celery
from django.conf import settings


# set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pinhead.settings")

app = Celery('pinhead')

app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
