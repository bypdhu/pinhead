# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import Http404
from django.shortcuts import render

from django.http import HttpResponse
from django.template import loader

from .models import Job


def index(request):
    jobs_list = Job.objects.all()
    template = loader.get_template('mycronjob/index.html')
    context = {
        'jobs_list': jobs_list
    }
    return HttpResponse(template.render(context, request))


def detail(request, job_id):
    try:
        job = Job.objects.get(pk=job_id)
    except Job.DoesNotExist:
        raise Http404("Job not found of id: " % job_id)
    return render(request, 'mycronjob/detail.html', {'job': job})


def results(request, job_id):
    return HttpResponse("you're looking at the results of job: %s" % job_id)


def histories(request, job_id):
    job = Job.objects.get(pk=job_id)
    history_s = [
        {
            'number': 1,
            'time': '2017-11-11 11:11:11'
        },
        {
            'number': 2,
            'time': '2017-11-11 22:22:22'
        }
    ]

    return render(request, 'mycronjob/history.html', {'job': job, 'histories': history_s})