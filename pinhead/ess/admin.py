# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import Bucket, Url
# Register your models here.

admin.site.register(Bucket)
admin.site.register(Url)
