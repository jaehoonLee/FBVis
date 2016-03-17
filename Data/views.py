from django.shortcuts import render, render_to_response
from datetime import datetime, timedelta
from Main.models import *
from django.http import HttpResponse
from django.utils import timezone

import pytz
import json
import operator

# Create your views here.
def treemap_data(request):

    key_word = ''
    if 'key_word' in request.GET:
        key_word = request.GET['key_word']

    result = {'name':'date', 'children':[]} #Date
    startdate = datetime.strptime("2016-02-04", '%Y-%m-%d')

    days = int(request.GET['days'])
    startdate = startdate + timedelta(days=days)

    eastern = pytz.timezone('US/Eastern')

    for i in range(0, 1):
        enddate = startdate + timedelta(days=1)

        if key_word == '':
            newsfeeds = NewsFeed.objects.filter(created_time__range=[startdate, enddate])
        else:
            newsfeeds = NewsFeed.objects.filter(created_time__range=[startdate, enddate], message__contains=key_word) # message__search=key_word

        val = {'name':startdate.strftime('%Y-%m-%d'), 'children':[], 'type':'date'}

        authors = newsfeeds.values("author").distinct()
        authors = [author_dic['author'] for author_dic in authors]

        for author in authors:
            author_newsfeeds = newsfeeds.filter(author=author)
            #subval = {'name':author, 'size':len(newsfeeds_author), 'type':'author'}
            subval = {'name':author, 'children':[], 'type':'author'} #Author
            for author_newsfeed in author_newsfeeds:
                created_time = author_newsfeed.created_time.astimezone(eastern).strftime("%Y-%m-%d %H:%M:%S")
                picture_exist = False if (author_newsfeed.picture_url == '') else True

                author_feed_val = {'name':author_newsfeed.type, 'size':1, 'type':'type', 'message':author_newsfeed.message, 'author':author, "author_img_url":author_newsfeed.author_img_url, "picture_url":author_newsfeed.picture_url, 'created_time':created_time,
                                   'comments':author_newsfeed.comments, 'likes':author_newsfeed.likes, 'picture_exist': picture_exist}
                subval['children'].append(author_feed_val)


            #print author
            val['children'].append(subval)


        result['children'].append(val)
        startdate = startdate + timedelta(days=1)


    return HttpResponse(json.dumps(result, indent=4, sort_keys=True))




def treemap_domain(request):
    timezone.now()
    startdate = datetime.strptime("2016-02-04", '%Y-%m-%d')

    all_authors = set()

    sets = set()
    lists = ['a', 'b', 'c']
    sets = sets.union(lists)
    print sets


    for i in range(0, 7):
        enddate = startdate + timedelta(days=1)
        newsfeeds = NewsFeed.objects.filter(created_time__range=[startdate, enddate])

        authors = newsfeeds.values("author").distinct()
        authors = [author_dic['author'] for author_dic in authors]

        all_authors = all_authors.union(authors)

        startdate = startdate + timedelta(days=1)

    print len(all_authors)

    return HttpResponse(json.dumps(list(all_authors), indent=4, sort_keys=True))



def barchart_data(request):
    key_word = ''
    if 'key_word' in request.GET:
        key_word = request.GET['key_word']

    result = []

    eastern = pytz.timezone('US/Eastern')
    startdate = datetime.strptime("2016-02-04", '%Y-%m-%d')
    startdate = eastern.localize(startdate)

    timediff = 1;
    for i in range(0, 7 * 24/timediff):
        enddate = startdate + timedelta(hours=timediff)
        if key_word == '':
            newsfeeds = NewsFeed.objects.filter(created_time__range=[startdate, enddate])
        else:
            newsfeeds = NewsFeed.objects.filter(created_time__range=[startdate, enddate], message__contains=key_word) # message__search=key_word


        val = {};
        val['date'] = startdate.strftime("%Y-%m-%d %H:%M:%S")
        val['count'] = len(newsfeeds)

        '''
        if len(newsfeeds) > 0:
            print newsfeeds[0].created_time.astimezone(eastern).strftime("%Y-%m-%d %H:%M:%S"), val['date']
        '''

        result.append(val)
        startdate = startdate + timedelta(hours=timediff)


    return HttpResponse(json.dumps(result, indent=4, sort_keys=True))

def famous_data(request):

    newsfeeds = NewsFeed.objects.all()
    authors = {}
    author_img = {}

    for newsfeed in newsfeeds:
        if not newsfeed.author in authors:
            authors[newsfeed.author] = 1
            author_img[newsfeed.author] = newsfeed.author_img_url

        else:
            authors[newsfeed.author] = authors[newsfeed.author] + 1
            #print "More Author"

    sorted_authors = sorted(authors.items(), key=operator.itemgetter(1), reverse=True)

    result = []
    for famous_people in sorted_authors[0:10]:
        result.append({"name": famous_people[0], "active": famous_people[1], "profile_url" : author_img[famous_people[0]]})

    return HttpResponse(json.dumps(result, indent=4, sort_keys=True))