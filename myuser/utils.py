#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Author  : bianbian
# @Site    : Asia/Shanghai
# @File    : utils.py
# @Software: bianbian's PyCharm
# @Time    : 2018/8/14 15:50

from django.core.cache import cache
from django.http import Http404


def set_tmp_user_to_cache(request, user):
    cache.set(request.session.session_key + 'user', user, 600)


def get_tmp_user_from_cache(request):
    if not request.session.session_key:
        return None
    user = cache.get(request.session.session_key + 'user')
    return user


def get_user_or_tmp_user(request):
    user = request.user
    tmp_user = get_tmp_user_from_cache(request)
    if user.is_authenticated:
        return user
    elif tmp_user:
        return tmp_user
    else:
        raise Http404("Not found this user")
