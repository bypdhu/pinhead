#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Author  : bianbian
# @Site    : Asia/Shanghai
# @File    : login.py
# @Software: bianbian's PyCharm
# @Time    : 2018/8/14 10:31

from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django.views.generic.edit import FormView

from .. import forms
from ..utils import set_tmp_user_to_cache, get_user_or_tmp_user

__all__ = ['UserLoginView']


class UserLoginView(FormView):
    template_name = 'myuser/login.html'
    form_class = forms.UserLoginForm

    def get(self, request, *args, **kwargs):
        print('you get it')
        self.request.session.set_test_cookie()
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        print('you post it')
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        if not self.request.session.test_cookie_worked():
            return HttpResponse(_("Please enable cookies and try again."))
        self.request.session.delete_test_cookie()
        set_tmp_user_to_cache(self.request, form.get_user())
        return redirect(self.get_success_url())

    def get_success_url(self):
        user = get_user_or_tmp_user(self.request)

        auth_login(self.request, user)
        return reverse('all:index')
