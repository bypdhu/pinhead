#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Author  : bianbian
# @Site    : Asia/Shanghai
# @File    : urls.py
# @Software: bianbian's PyCharm
# @Time    : 2018/7/2 15:05

from django.conf.urls import url

from filetrans import views

app_name = 'filetrans'

urlpatterns = [
    url(r'^$', views.upload_accept, name='upload-accept'),
    url(r'^upload/accept$', views.upload_accept, name='upload-accept'),
    url(r'^upload/complete$', views.upload_complete, name='upload-complete'),
]
