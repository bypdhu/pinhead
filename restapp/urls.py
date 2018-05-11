#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Author  : bianbian
# @Site    : Asia/Shanghai
# @File    : urls.py
# @Software: bianbian's PyCharm
# @Time    : 2018/5/11 16:59

from __future__ import unicode_literals
from django.conf.urls import url, include
from rest_framework import routers

from restapp import views

app_name = 'restapp'

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
]
