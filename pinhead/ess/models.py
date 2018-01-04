# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class Bucket(models.Model):
    name = models.CharField(max_length=127, unique=True)
    status = models.BooleanField(choices=((True, "启用"), (False, "禁用")), default=True)
    access_key = models.CharField(max_length=127)
    access_secret = models.CharField(max_length=127)
    inner_url = models.URLField(verbose_name='inner base url', blank=True)
    outer_url = models.URLField(verbose_name='outer base url', blank=True)


class Url(models.Model):
    url = models.URLField()
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    save_to_disk = models.BooleanField(default=True)
    file_path = models.CharField(max_length=127, blank=save_to_disk)
    

class DownloadUrlHistory(models.Model):
    url = models.URLField()
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    times = models.IntegerField(verbose_name="下载次序", default=1)
    check_md5 = models.BooleanField(choices=((True, "检查MD5"), (False, "不检查MD5")), default=True)
    md5 = models.CharField(max_length=63, blank=(not check_md5))
    modified = models.BooleanField(choices=((True, "修改"), (False, "未修改")), default=False)