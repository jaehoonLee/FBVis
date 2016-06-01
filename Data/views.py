#-*- coding: utf-8 -*-
from django.shortcuts import render, render_to_response
from datetime import datetime, timedelta
from Main.models import *
from django.http import HttpResponse
from django.utils import timezone

from operator import itemgetter
from stop_words import get_stop_words
from django.views.decorators.csrf import csrf_exempt

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

        for author_idx, author in enumerate(authors):
            author_newsfeeds = newsfeeds.filter(author=author)
            #subval = {'name':author, 'size':len(newsfeeds_author), 'type':'author'}
            subval = {'name':author, 'children':[], 'type':'author'} #Author
            for feed_idx, author_newsfeed in enumerate(author_newsfeeds):
                created_time = author_newsfeed.created_time.astimezone(eastern).strftime("%Y-%m-%d %H:%M:%S")
                picture_exist = False if (author_newsfeed.picture_url == '') else True

                author_feed_val = {'name':author_newsfeed.type, 'size':1, 'type':'type', 'message':author_newsfeed.message, 'author':author, "author_img_url":author_newsfeed.author_img_url, "picture_url":author_newsfeed.picture_url, 'created_time':created_time,
                                   'comments':author_newsfeed.comments, 'likes':author_newsfeed.likes, 'picture_exist': picture_exist,
                                   'fbid':author_newsfeed.fbid

                                   }
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


@csrf_exempt
def removed_barchart_data(request):

    name_list = request.POST.getlist('delete_authors[]')
    result = []

    eastern = pytz.timezone('US/Eastern')
    startdate = datetime.strptime("2016-02-04", '%Y-%m-%d')
    startdate = eastern.localize(startdate)

    timediff = 1;
    for i in range(0, 7 * 24/timediff):
        enddate = startdate + timedelta(hours=timediff)
        #newsfeeds = NewsFeed.objects.filter(created_time__range=[startdate, enddate], author__in=name_list)
        newsfeeds = NewsFeed.objects.filter(created_time__range=[startdate, enddate]).exclude(author__in=name_list)

        val = {};
        val['date'] = startdate.strftime("%Y-%m-%d %H:%M:%S")
        val['count'] = len(newsfeeds)

        result.append(val)
        startdate = startdate + timedelta(hours=timediff)


    return HttpResponse(json.dumps(result, indent=4, sort_keys=True))

def word_cloud_data(request):
    word_dic = {}
    word_lst = []

    startdate = datetime.strptime("2016-02-04", '%Y-%m-%d')
    enddate = startdate + timedelta(days=7)

    newsfeeds = NewsFeed.objects.filter(created_time__range=[startdate, enddate])
    stop_words = get_stop_words('en')

    for newsfeed in newsfeeds:
        for word in newsfeed.message.split(" "):
            word = word.lower() #Not Case Sensitive
            if word == '':
                continue

            if word in word_dic:
                word_dic[word] += 1
            else:
                word_dic[word] = 1



    word_sorted = sorted(word_dic.items(), key=itemgetter(1), reverse=True)

    for value in word_sorted:
        if not value[0].lower() in stop_words:
            word_lst.append({'text':value[0], 'size':value[1]})
        if len(word_lst) >= 100:
            break

#    for word in word_lst:
#        print word["text"], word["size"]


    return json.dumps(word_lst, indent=4, sort_keys=True)


    '''
    if 'key' in result :
        result['key'] = 1;
    else:
        result['key'] += 1;
    '''

    #return HttpResponse(json.dumps(word_lst, indent=4, sort_keys=True))


@csrf_exempt
def filtered_word_cloud_data(request):
    word_dic = {}
    word_lst = []

    delete_authors = request.POST.getlist('delete_authors[]')

    startdate = datetime.strptime("2016-02-04", '%Y-%m-%d')
    enddate = startdate + timedelta(days=7)

    newsfeeds = NewsFeed.objects.filter(created_time__range=[startdate, enddate])
    stop_words = get_stop_words('en')

    skip = 0
    for newsfeed in newsfeeds:
        if newsfeed.author in delete_authors:
            #skip = skip + 1
            continue

        for word in newsfeed.message.split(" "):
            word = word.lower() #Not Case Sensitive
            if word == '':
                continue

            if word in word_dic:
                word_dic[word] += 1
            else:
                word_dic[word] = 1

    #print skip

    word_sorted = sorted(word_dic.items(), key=itemgetter(1), reverse=True)

    #for value in word_sorted[0:10]:
    #    print value[0], value[1]

    for value in word_sorted:
        if not value[0].lower() in stop_words:
            word_lst.append({'text':value[0], 'size':value[1]})
        if len(word_lst) >= 100:
            break

    #for text in word_lst[0:10]:
    #    print text['text'], text['size']

    print len(word_lst)
    return HttpResponse(json.dumps(word_lst, indent=4, sort_keys=True))




def famous_data(request):

    newsfeeds = NewsFeed.objects.all()
    authors = {}
    author_img = {}
    author_id = {}


    for newsfeed in newsfeeds:
        if not newsfeed.author in authors:
            authors[newsfeed.author] = 1
            author_img[newsfeed.author] = newsfeed.author_img_url
            author_id[newsfeed.author] = newsfeed.fbid.split("_")[0]
        else:
            authors[newsfeed.author] = authors[newsfeed.author] + 1
            #print "More Author"

    sorted_authors = sorted(authors.items(), key=operator.itemgetter(1), reverse=True)

    result = []
    for famous_people in sorted_authors[0:100]:
        result.append({"name": famous_people[0], "active": famous_people[1], "profile_url" : author_img[famous_people[0]], "author_id":author_id[famous_people[0]]})


    return HttpResponse(json.dumps(result, indent=4, sort_keys=True))
