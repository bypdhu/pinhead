#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Author  : bianbian
# @Site    : Asia/Shanghai
# @File    : forms.py
# @Software: bianbian's PyCharm
# @Time    : 2018/8/14 13:19

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label=_("Username"), max_length=100)
    password = forms.CharField(label=_('Password'), widget=forms.PasswordInput, max_length=128, strip=False)
