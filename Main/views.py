#-*- coding: utf-8 -*-
from django.shortcuts import render, render_to_response
from models import *
from datetime import datetime, timedelta
from django.utils import timezone
from django.http import HttpResponse
from django.template import RequestContext
from Data.views import word_cloud_data

import facebook
import json
import pytz

token = 'CAACEdEose0cBACUaOP9dH85WOJxhXpxEV89chFuGqGVTEsvJ2jCr8cTrFrRSD7R2KK82GiS0X3Nwle7Wc1DQPbsLyYwOpj3RNsTAjU8IUzZCpKWJvQhYyGxW8vhS89kaxRs1H8qpPoLoQW6f8LQVXyYfUZBtSAAZAonFX78HHBWOlZCnk28bFWHCrcWtsF1GprZAJbL93UwZDZD'
crawl_start = '2016-02-12'
crawl_end = '2016-02-13'


#TODO:Resoluation for website

def test(request):
    return render_to_response('tiptest.html', RequestContext(request))

def main(request):
    eng_word_lst = word_cloud_data(True)
    not_eng_word_lst = word_cloud_data(False)
    return render_to_response('index.html', RequestContext(request, {'eng_word_lst': eng_word_lst, 'not_eng_word_lst':not_eng_word_lst,
                                                                     'request':request, 'user': request.user}))

def manual(request):

    newsfeeds = {}
    if request.user.is_authenticated():
        for newsfeed in request.user.newsfeed_set.all():
            key = newsfeed.created_time.strftime("%Y-%m-%d")
            if not key in newsfeeds:
                newsfeeds[key] = 0
            else :
                newsfeeds[key] = newsfeeds[key] + 1

    print newsfeeds

    return render_to_response('manual.html', RequestContext(request, {'user':request.user, 'newsfeeds':sorted(newsfeeds.items())}))


def word_cloud(request):
    return render_to_response('word_cloud2.html')