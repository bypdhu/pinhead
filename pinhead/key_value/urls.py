from django.conf.urls import url

from . import views

app_name = 'app_keyvalues'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^keyvalue/$', views.keyvalue_index, name='keyvalue_index'),
    url(r'^value/$', views.value_index, name='value_index'),
]
