# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from .models import SomeData


# Create your views here.


def index(request):
    somedatas = SomeData.objects.all()
    page = {'datas': somedatas}

    return render(request, 'pagetest/index.html', page)
