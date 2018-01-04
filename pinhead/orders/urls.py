#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Author  : bianbian
# @Site    : Asia/Shanghai
# @File    : urls.py
# @Software: bianbian's PyCharm
# @Time    : 2018/1/2 17:47

from django.conf.urls import url
from . import views


app_name = 'orders'

urlpatterns = [
   url(r'^create/$', views.order_create, name='order_create'),
]