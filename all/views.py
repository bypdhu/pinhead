#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Author  : bianbian
# @Site    :
# @File    : views.py
# @Software: bianbian's PyCharm
# @Time    : 2017/12/21 15:00

from __future__ import unicode_literals

from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required(login_url='/myuser/login')
def index(request):
    apps = [
        # these four usage are all OK.. when used in html like <a href="{{url}}" />
        # {'name': 'admin', 'url': 'admin'},
        # {'name': 'admin', 'url': 'admin/'},
        # {'name': 'admin', 'url': '/admin'},
        # {'name': 'admin', 'url': '/admin/'},

        {'name': 'admin', 'url': '/admin'},
        {'name': 'ess', 'url': '/ess'},
        {'name': 'key value', 'url': '/keyvalue'},
        {'name': 'my cron job', 'url': '/cronjob'},
        {'name': 'my shop', 'url': '/shop'},
        {'name': 'page test', 'url': '/pagetest'},
        {'name': 'rest app', 'url': '/restapp'},
        {'name': 'file trans', 'url': '/filetrans'},
    ]
    return render(request, 'all/index.html', {'apps': apps})
