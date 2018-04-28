# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import SomeData


# Create your views here.

def change_to_int(ch, int_d=5):
    if not isinstance(ch, int):
        try:
            ch = int(ch)
        except Exception:
            ch = int_d
    return ch


def index(request):
    per_page_num = request.GET.get('per_page_num', 3)
    per_page_num = change_to_int(per_page_num, 3)
    page_num = request.GET.get('page_num', 1)
    page_num = change_to_int(page_num, 1)

    somedata = SomeData.objects.all()
    paginator = Paginator(somedata, per_page_num)
    try:
        datas = paginator.page(page_num)
    except PageNotAnInteger:
        datas = paginator.page(1)
    except EmptyPage:
        datas = paginator.page(paginator.num_pages)

    page = {'datas': datas}

    return render(request, 'pagetest/index.html', page)
