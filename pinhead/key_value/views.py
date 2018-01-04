# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from .models import KeyValue, Value


def index(request):
    key_value_list = KeyValue.objects.all()
    return render(request, 'key_value/index.html', {'key_value_list': key_value_list})


def keyvalue_index(request):
    key_value_list = KeyValue.objects.all()
    return render(request, 'key_value/keyvalue_index.html', {'key_value_list': key_value_list})


def value_index(request):
    value_list = Value.objects.all()
    return render(request, 'key_value/value_index.html', {"value_list": value_list})