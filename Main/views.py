from django.shortcuts import render, render_to_response
from models import *
from datetime import datetime, timedelta
from django.utils import timezone
from django.http import HttpResponse
from django.template import RequestContext
from operator import itemgetter
from stop_words import get_stop_words

import facebook
import json
import pytz

token = 'CAACEdEose0cBACUaOP9dH85WOJxhXpxEV89chFuGqGVTEsvJ2jCr8cTrFrRSD7R2KK82GiS0X3Nwle7Wc1DQPbsLyYwOpj3RNsTAjU8IUzZCpKWJvQhYyGxW8vhS89kaxRs1H8qpPoLoQW6f8LQVXyYfUZBtSAAZAonFX78HHBWOlZCnk28bFWHCrcWtsF1GprZAJbL93UwZDZD'
crawl_start = '2016-02-12'
crawl_end = '2016-02-13'


def test(request):
    return render_to_response('test.html', RequestContext(request))


def main(request):
    word_lst = word_cloud_data(request)
    #print word_lst
    return render_to_response('index.html', RequestContext(request, {'word_lst': word_lst}))
    #return render_to_response('word_cloud.html')

def word_cloud(request):
    return render_to_response('word_cloud.html')

def word_cloud_data(request):
    word_dic = {}
    word_lst = []
    startdate = datetime.strptime("2016-02-04", '%Y-%m-%d')
    enddate = startdate + timedelta(days=7)
    newsfeeds = NewsFeed.objects.filter(created_time__range=[startdate, enddate])
    stop_words = get_stop_words('en')

    for newsfeed in newsfeeds:
        #print newsfeed.message

        for word in newsfeed.message.split(" "):
            if word == '':
                continue

            if word in word_dic:
                word_dic[word] += 1
            else:
                word_dic[word] = 1

    word_sorted = sorted(word_dic.items(), key=itemgetter(1), reverse=True)

    for value in word_sorted:
        if not value[0] in stop_words:
            word_lst.append({'text':value[0], 'size':value[1]})
        if len(word_lst) >= 100:
            break



    return json.dumps(word_lst, indent=4, sort_keys=True)


    '''
    if 'key' in result :
        result['key'] = 1;
    else:
        result['key'] += 1;
    '''

    return HttpResponse(json.dumps(word_lst, indent=4, sort_keys=True))


# TODO : have to update some newsfeed with different likes and comments.(count will be reupdated)

def crawl(request):
    timezone.now()
    graph = facebook.GraphAPI()
    graph_id = 'v2.2/me/home?access_token=' + token + '&since='+ crawl_start + '&until=' + crawl_end + '&limit=100' #
    post = graph.get_object(id=graph_id)

    '''
    for newsfeed in post['data']:
        #print json.dumps(data, indent=4, sort_keys=True)

        message = ''
        if 'message' in newsfeed:
            message = newsfeed['message']
        fbid = newsfeed['id']
        author = newsfeed['from']["name"]
        created_time = newsfeed['created_time']
        created_time = datetime.strptime(created_time, '%Y-%m-%dT%H:%M:%S+0000')
        created_time = pytz.utc.localize(created_time)
        eastern = pytz.timezone('US/Eastern')
        created_time = created_time.astimezone(eastern)


        try:
            news = NewsFeed.objects.get(fbid=fbid)
        except:
            NewsFeed.objects.create_newsfeed(fbid, message, created_time, author)

    '''






    shares = models.IntegerField()
    likes = models.IntegerField()
    comments = models.IntegerField()

    zero_count = 0
    while graph_id != '':

        if len(post['data']) == 0:
            break

        count = 0
        for newsfeed in post['data']:
            #print json.dumps(post['data'], indent=4, sort_keys=True)

            message = ''
            if 'message' in newsfeed:
                message = newsfeed['message']
            fbid = newsfeed['id']
            author = newsfeed['from']["name"]
            author_id = newsfeed['from']["id"]
            created_time = newsfeed['created_time']
            updated_time = newsfeed['updated_time']

            created_time = datetime.strptime(created_time, '%Y-%m-%dT%H:%M:%S+0000')
            updated_time = datetime.strptime(updated_time, '%Y-%m-%dT%H:%M:%S+0000')
            created_time = pytz.utc.localize(created_time)
            updated_time = pytz.utc.localize(updated_time)
            eastern = pytz.timezone('US/Eastern')
            created_time = created_time.astimezone(eastern)
            updated_time = updated_time.astimezone(eastern)

            picture_url = ''
            if 'picture' in newsfeed:
                picture_url = newsfeed["picture"]

            link_url = ''
            if 'link' in newsfeed:
                link_url = newsfeed["link"]

            link_name = ''
            if 'name' in newsfeed:
                link_name = newsfeed['name']

            link_description = ''
            if 'description' in newsfeed:
                link_description = newsfeed['description']

            link_caption = ''
            if 'caption' in newsfeed:
                link_caption = newsfeed['caption']

            type = ''
            if 'type' in newsfeed:
                type = newsfeed['type']

            status_type = ''
            if 'status_type' in newsfeed:
                status_type = newsfeed['status_type']

            shares = 0
            if 'shares' in newsfeed:
                shares = newsfeed['shares']['count']

            story = ''
            if 'story' in newsfeed:
                story = newsfeed['story']


            '''profile img url'''

            author_img_url = ''
            try :
                author_img_url = graph.get_object('v2.2/' + author_id + '/picture?width=70&height=70&access_token=' + token)
                author_img_url = author_img_url['url']
            except :
                print "author found error:" + author_id

            '''count likes'''
            feed_id = newsfeed['id'].split('_')[1]
            #print newsfeed['id'], feed_id
            likes_count = 0
            try:
                likes = graph.get_object('v2.2/' + feed_id + '/likes?summary=true&access_token=' + token)
                if 'summary' in likes:
                    likes_count = likes["summary"]["total_count"]
            except:
                print "like found error:" + newsfeed['id']


            '''count comments'''
            comments_count = 0
            try:
                comments = graph.get_object('v2.2/' + feed_id + '/comments?summary=true&access_token=' + token)
                if 'summary' in comments:
                    comments_count = comments["summary"]["total_count"]

            except:
                print "comment found error:" + newsfeed['id']


            #print likes_count, comments_count

            try:
                NewsFeed.objects.get(fbid=fbid)
            except:
                NewsFeed.objects.create_newsfeed(fbid, message, created_time, updated_time, author, author_id, picture_url, link_url, link_name, link_description, link_caption, type, status_type, shares, likes_count, comments_count, author_img_url, story)
                count = count + 1


        #print json.dumps(post, indent=4, sort_keys=True)
        graph_id = post['paging']['next'].split('https://graph.facebook.com/')[1]

        if graph_id[-3:]=='%3F':
            graph_id = graph_id[:-3]
        print count, ":", graph_id
        if count == 0:
            zero_count = zero_count + 1

        if zero_count == 10:
            break

        post = graph.get_object(id=graph_id)


    return render_to_response('index.html')


def checkDatebase(request):
    timezone.now()
    startdate = datetime.strptime("2016-02-05", '%Y-%m-%d')
    for i in range(0, 20):
        enddate = startdate + timedelta(days=1)
        news = NewsFeed.objects.filter(created_time__range=[startdate, enddate])
        print startdate, len(news)
        startdate = startdate - timedelta(days=1)

    return render_to_response('index.html')



def update_image_url(request):
    graph = facebook.GraphAPI()
    newsfeeds = NewsFeed.objects.all()
    for newsfeed in newsfeeds:
        graph_id = 'v2.2/' + newsfeed.author_id + '/picture?width=70&height=70&access_token=' + token + '' #
        post = graph.get_object(id=graph_id)
        newsfeed.author_img_url = post['url']
        newsfeed.save()

    return HttpResponse("Success")




