#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Author  : bianbian
# @Site    : 
# @File    : urls.py
# @Software: bianbian's PyCharm
# @Time    : 2017/12/20 17:52

from django.conf.urls import url
from . import views

app_name = 'shop'

urlpatterns = [
    url(r'^category/(?P<category_slug>[-\w]+)/$', views.product_list, name='product_list_by_category'),
    url(r'^category/(?P<c_id>\d+)/product/(?P<slug>[-\w]+)/$', views.product_detail, name='product_detail'),
    url(r'^category/$', views.product_list, name='product_list'),

    url(r'^$', views.product_list, name='index'),

]