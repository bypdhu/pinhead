#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Author  : bianbian
# @Site    : Asia/Shanghai
# @File    : context_processors.py
# @Software: bianbian's PyCharm
# @Time    : 2018/1/2 16:25

from .cart import Cart


def cart_template(request):
    return {'cart_cp': Cart(request)}
