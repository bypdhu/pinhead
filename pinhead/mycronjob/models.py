# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class Job(models.Model):
    id = models.CharField(max_length=128, primary_key=True)
    name = models.CharField(max_length=50)
    cron_expr = models.CharField(max_length=128)
    status = models.IntegerField(default=0, blank=True)  # 0:create, 1:update, 2:delete, 3:run, 4:pause, 5:stop
    start_time = models.DateTimeField('start time', blank=True)
    last_run_time = models.DateTimeField('last run time', blank=True)
    next_run_time = models.DateTimeField('next run time', blank=True)
    description = models.CharField(max_length=512, blank=True, default="")
