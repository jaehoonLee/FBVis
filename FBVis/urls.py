"""FBVis URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from Main.views import *
from Data.views import *
from Multi.views import *

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', main),
    url(r'^test/$', test),
    url(r'^word_cloud/', word_cloud),
    url(r'^word_cloud_data/', word_cloud_data),

    url(r'^treemap_data/', treemap_data),
    url(r'^treemap_domain/', treemap_domain),

    url(r'^barchart_data/', barchart_data),
    url(r'^famous_data/', famous_data),

    url(r'^checkDatebase/', checkDatebase),
    url(r'^crawl/', crawl),
    url(r'^update_image_url/', update_image_url),
    url(r'^multi_treemap/(?P<day>[0-9])', treemap),
]
