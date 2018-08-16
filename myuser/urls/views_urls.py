#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Author  : bianbian
# @Site    : Asia/Shanghai
# @File    : view_urls.py
# @Software: bianbian's PyCharm
# @Time    : 2018/8/14 10:25

from __future__ import absolute_import

from django.conf.urls import url

from .. import views

app_name = 'myuser'

urlpatterns = [
    url(r'^login/$', views.UserLoginView.as_view(), name='login'),
    url(r'^logout/$', views.UserLogoutView.as_view(), name='logout'),

]
