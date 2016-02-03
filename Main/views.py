from django.shortcuts import render, render_to_response
from models import *
from datetime import datetime, timedelta
from django.utils import timezone
from django.http import HttpResponse

import facebook
import json
import pytz

token = 'CAACEdEose0cBAFwAxk5wyvQjLSYZCPgzNQZCGZC8uZCubwck5ynnZBWX1dbx4V0uINnJuZA2Etnh61iRmA2wto0KqBdT0WHyU919bZBYeDE3HfA5sZBxQUv3ZAVeQ3zjvZBSgHsT073W3IrFJvTPxeS7RafaeqgXj3KBZBmr83pEGwLy84nAZBnuOYPhwfH7y5f4QpeUIXSZA6dMQSwZDZD'

def main(request):
    return render_to_response('index.html')


def treemap_data(request):
    result = {'name':'date', 'children':[]}
    startdate = datetime.strptime("2016-02-03", '%Y-%m-%d')
    for i in range(0, 4):
        enddate = startdate + timedelta(days=1)
        newsfeeds = NewsFeed.objects.filter(created_time__range=[startdate, enddate])
        startdate = startdate - timedelta(days=1)

        val = {'name':startdate.strftime('%Y-%m-%d'), 'children':[], 'type':'date'}

        authors = newsfeeds.values("author").distinct()
        authors = [author_dic['author'] for author_dic in authors]

        for author in authors:
            author_newsfeeds = newsfeeds.filter(author=author)
            #subval = {'name':author, 'size':len(newsfeeds_author), 'type':'author'}
            subval = {'name':author, 'children':[], 'type':'author'}
            for author_newsfeed in author_newsfeeds:
                author_feed_val = {'name':author_newsfeed.type, 'size':1, 'type':'type', 'message':author_newsfeed.message, 'author':author, "author_img_url":author_newsfeed.author_img_url, "picture_url":author_newsfeed.picture_url}
                subval['children'].append(author_feed_val)


            #print author
            val['children'].append(subval)


        result['children'].append(val)


    return HttpResponse(json.dumps(result, indent=4, sort_keys=True))


def crawl(request):
    timezone.now()
    graph = facebook.GraphAPI()
    graph_id = 'v2.2/me/home?access_token=' + token + '&since=2016-02-03&until=2016-02-04&limit=100' #
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



            '''profile img url'''

            author_img_url = graph.get_object('v2.2/' + author_id + '/picture?width=70&height=70&access_token=' + token)
            author_img_url = author_img_url['url']

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
                NewsFeed.objects.create_newsfeed(fbid, message, created_time, updated_time, author, author_id, picture_url, link_url, link_name, link_description, link_caption, type, status_type, shares, likes_count, comments_count, author_img_url)
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
    startdate = datetime.strptime("2016-02-03", '%Y-%m-%d')
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




