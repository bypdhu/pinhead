#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Author  : bianbian
# @Site    : Asia/Shanghai
# @File    : urls.py
# @Software: bianbian's PyCharm
# @Time    : 2018/4/28 16:50

from django.conf.urls import url
from . import views

app_name = 'pagetest'

urlpatterns = [
    url(r'^$', view=views.index, name='index of pagetest')
]
