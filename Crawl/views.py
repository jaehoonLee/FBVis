from datetime import datetime
from django.http import HttpResponse
from django.shortcuts import render, render_to_response
from Main.models import *
from Data.models import *
from django.utils import timezone

# Create your views here.
# TODO : have to update some newsfeed with different likes and comments.(count will be reupdated)
import facebook
import pytz

token = 'EAACEdEose0cBAMbH3831WPwDiGTZCZAl4q5GQgJjHaPXhdP2GfUCnCLjoBChgiE35U5JdBssIlPmGnBEpLI9tvFGZC6hXmADuPZB47QuQr6BrJeAYq0WepgMV0r3vRgmQuVfMOmTuNofZAvQamz0niXw1qsZABgwo5G4NWSUqu5gZDZD'
crawl_start = '2016-10-31'
crawl_end = '2016-11-01'


def crawl_new_api(request):
    graph = facebook.GraphAPI()
    graph_id = 'v2.0/me/friends?access_token=' + token
    post = graph.get_object(id=graph_id)

    friends = []
    friends = friends + post["data"]
    while post["paging"].has_key("next"):
        friends = friends + post["data"]
        graph_id = post["paging"]["next"].split("https://graph.facebook.com/")[1]
        post = graph.get_object(id=graph_id)

        print friends
        print len(friends), len(post["data"])


    return HttpResponse("Hello")



def crawl(request):

    token = request.POST["access-token"]

    timezone.now()
    graph = facebook.GraphAPI(access_token=token, version='2.2')
    #graph_id = 'me/home?access_token=' + token + '&since='+ crawl_start + '&until=' + crawl_end + '&limit=100' #
    graph_id='me/home?since='+ crawl_start + '&until=' + crawl_end +"&limit=50"
    print graph_id
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
            #author = newsfeed['from']["name"]
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


            '''count likes'''
            feed_id = newsfeed['id'].split('_')[1]
            #print newsfeed['id'], feed_id
            likes_count = 0
            try:
                likes = graph.get_object(feed_id + '/likes?summary=true&access_token=' + token)
                if 'summary' in likes:
                    likes_count = likes["summary"]["total_count"]
            except:
                print "like found error:" + newsfeed['id']


            '''count comments'''
            comments_count = 0
            try:
                comments = graph.get_object(feed_id + '/comments?summary=true&access_token=' + token)
                if 'summary' in comments:
                    comments_count = comments["summary"]["total_count"]

            except:
                print "comment found error:" + newsfeed['id']


            #print likes_count, comments_count

            try:
                NewsFeed.objects.get(fbid=fbid)
            except:
                feed = NewsFeed.objects.create_newsfeed(fbid, message, created_time, updated_time, author_id, picture_url, link_url, link_name, link_description, link_caption, type, status_type, shares, likes_count, comments_count, story)
                feed.owner = request.user
                feed.save()

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

        graph_id = graph_id.split("/", 1)[1].split("&")
        graph_id = graph_id[0] + '&' + graph_id[1] + '&limit=75'
        print graph_id

        try:
            post = graph.get_object(id=graph_id)
        except:
            print "ERROR Maintype was not text, image, or querystring"

    return render_to_response('index.html')


def checkDatebase(request):
    timezone.now()
    startdate = datetime.strptime("2016-02-05", '%Y-%m-%d')
    for i in range(0, 20):
        enddate = startdate + datetime.timedelta(days=1)
        news = NewsFeed.objects.filter(created_time__range=[startdate, enddate])
        print startdate, len(news)
        startdate = startdate - datetime.timedelta(days=1)

    return render_to_response('index.html')



def update_image_url(request):
    graph = facebook.GraphAPI(access_token=token, version='2.2')
    newsfeeds = NewsFeed.objects.all()
    for newsfeed in newsfeeds:
        graph_id = newsfeed.author_id + '/picture?width=70&height=70' #
        post = graph.get_object(id=graph_id)
        newsfeed.author_img_url = post['url']
        newsfeed.save()

    return HttpResponse("Success")


def update_like_comment(request):
    graph = facebook.GraphAPI(access_token=token, version='2.2')
    newsfeeds = NewsFeed.objects.all()
    for newsfeed in newsfeeds:
        feed_id = newsfeed.fbid.split('_')[1]
        print feed_id
        likes_count = 0
        try:
            likes = graph.get_object(feed_id + '/likes?summary=true&access_token=' + token)
            if 'summary' in likes:
                likes_count = likes["summary"]["total_count"]
        except:
            print "like found error:" + newsfeed.fbid

        '''count comments'''
        comments_count = 0
        try:
            comments = graph.get_object(feed_id + '/comments?summary=true&access_token=' + token)
            if 'summary' in comments:
                comments_count = comments["summary"]["total_count"]

        except:
            print "comment found error:" + newsfeed.fbid

        newsfeed.likes = likes_count
        newsfeed.comments = comments_count
        newsfeed.save()

    return HttpResponse("Success")


def update_friend_info(request):
    newsfeeds = NewsFeed.objects.all()
    for newsfeed in newsfeeds:
        try:
            friend = FacebookFriend.objects.get(fbid=newsfeed.author_id)
        except:
            print newsfeed.author
            FacebookFriend.objects.create_facebookfriend(name=newsfeed.author, fbid=newsfeed.author_id, img_url=newsfeed.author_img_url, close=False)

    return HttpResponse("Success")


def update_owner_info(request):
    newsfeeds = NewsFeed.objects.all()
    for newsfeed in newsfeeds:
        newsfeed.owner = request.user
        newsfeed.save()

    return HttpResponse("Success")
