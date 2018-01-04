from django.conf.urls import url

from . import views

app_name = 'ess'

urlpatterns = [
    url(r'^$', views.index, name='index'),

    url(r'^download/?$', views.download, name='download'),
    url(r'^download/display/?$', views.get_file_content_from_url, name='download_display'),
    url(r'^download/history/?$', views.get_download_url_history, name='download_history'),
    url(r'^download/history/(?P<url>.*)/?$', views.get_one_download_url_history, name='download_history_of_url'),

    url(r'^upload/$', views.upload, name='upload'),

    url(r'^bucket/$', views.list_bucket, name='bucket'),
    url(r'^bucket/create/$', views.create_bucket, name='bucket_create'),

]

