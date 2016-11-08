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
from Main.views import *
from Data.views import *
from Multi.views import *
from FBAuth.views import *
from Crawl.views import *

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', main),
    url(r'^test/$', test),
    url(r'^manual/', manual),
    url(r'^word_cloud/', word_cloud),
    url(r'^word_cloud_data/', word_cloud_data),
    url(r'^filtered_word_cloud_data/(?P<is_eng>[0-9])', filtered_word_cloud_data),

    url(r'^treemap_data/', treemap_data),
    url(r'^treemap_domain/', treemap_domain),
    url(r'^barchart_data/', barchart_data),
    url(r'^removed_barchart_data/', removed_barchart_data),
    url(r'^famous_data/', famous_data),

    url(r'^checkDatebase/', checkDatebase),
    url(r'^crawl/', crawl),
    url(r'^crawl_new_api/', crawl_new_api),
    url(r'^update_image_url/', update_image_url),
    url(r'^update_like_comment/', update_like_comment),
    url(r'^update_friend_info/', update_friend_info),
    url(r'^update_owner_info/', update_owner_info),

    url(r'^multi_treemap/(?P<day>[0-9])', treemap),
    url(r'^pallette/', pallette),
    url(r'^pallette_signal/', pallette_signal),
    url(r'^pallette_assign/', pallette_assign),
    url(r'^treemap_signal/(?P<day>[0-9])', treemap_signal),
    url(r'^treemap_assign/(?P<fbid>\w+)', treemap_assign),

    url('', include('django.contrib.auth.urls', namespace='auth')),
    url(r'^social/', include('social.apps.django_app.urls', namespace='social')),
    url(r'^home/', home, name='home'),

]
