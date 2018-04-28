"""pinhead URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin

from . import settings

urlpatterns = [

    ######  url for admin   #########
    url(r'^admin/', admin.site.urls),
    #################################

    ###### url for mycronjob #########
    url(r'^cronjob/', include('mycronjob.urls')),
    ###################################

    ####### url for key_value #########
    url(r'^keyvalue/', include('key_value.urls')),
    #######################################

    ######## url for ess ################
    url(r'^ess/', include('ess.urls')),
    #####################################

    ######## url for myshop-cart ################
    url(r'^cart/', include('cart.urls', namespace='cart')),
    #####################################

    ######## url for myshop-orders ################
    # url(r'^shop/', include('myshop.urls', namespace='myshop')),
    url(r'^orders/', include('orders.urls', namespace='orders')),
    #####################################

    ######## url for myshop ################
    # url(r'^shop/', include('myshop.urls', namespace='myshop')),
    url(r'^shop/', include('myshop.urls')),
    #####################################

    ######## url for pagetest ################
    url(r'^pagetest/', include('pagetest.urls')),
    #####################################

    #######  url for all   ##########
    url(r'^', include('all.urls')),
    #################################

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)