#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Author  : bianbian
# @Site    : 
# @File    : urls.py
# @Software: bianbian's PyCharm
# @Time    : 2017/12/21 15:14

from django.conf.urls import url
from . import views

app_name = 'all'

urlpatterns = [
    url(r'^$', views.index, name='index'),
]