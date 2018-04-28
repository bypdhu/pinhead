#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Author  : bianbian
# @Site    : Asia/Shanghai
# @File    : urls.py
# @Software: bianbian's PyCharm
# @Time    : 2018/1/2 18:05

from django.conf.urls import url
from . import views

app_name = 'cart'

urlpatterns = [
    url(r'^add/(?P<product_id>[-\w]+)$', views.cart_add, name='cart_add'),
    url(r'^remove/(?P<product_id>[-\w]+)$', views.cart_remove, name='cart_remove'),
    url(r'^$', views.cart_detail, name='cart_detail'),


]