from django.conf.urls import url
# from django.contrib import admin

from . import views

app_name = 'cronjob'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<job_id>[0-9a-zA-Z]+)/$', views.detail, name='detail11'),
    url(r'^(?P<job_id>[0-9a-zA-Z]+)$', views.detail, name='detail22'),
    url(r'^(?P<job_id>[0-9a-zA-Z]+)/results/$', views.results, name='results1'),
    url(r'^(?P<job_id>[0-9a-zA-Z]+)/results$', views.results, name='results2'),
    url(r'^(?P<job_id>[0-9a-zA-Z]+)/history/$', views.histories, name='history11')
]
