from django.db import models
from django.contrib import admin

# Create your models here.
class NewsFeedManager(models.Manager):
    def create_newsfeed(self, fbid, message, created_time, updated_time, author, author_id, picture_url, link_url, link_name, link_description, link_caption, type, status_type, shares, likes, comments, author_img_url, story):
        newsfeed = self.model(fbid=fbid, message=message, created_time=created_time, updated_time= updated_time, author=author, author_id=author_id,
                                picture_url=picture_url, link_url=link_url, link_name=link_name, link_description=link_description, link_caption=link_caption, type=type, status_type=status_type,
                                shares=shares, likes=likes, comments=comments, author_img_url=author_img_url, story=story)
        newsfeed.save()
        return newsfeed

class NewsFeed(models.Model):
    fbid = models.CharField(max_length=255, unique=True)
    created_time = models.DateTimeField()
    updated_time = models.DateTimeField()

    author_id = models.CharField(max_length=255)

    story = models.CharField(max_length=255)

    message = models.TextField()
    picture_url = models.TextField()
    link_url = models.TextField()
    link_name = models.TextField()
    link_description = models.TextField()
    link_caption = models.TextField()

    type = models.CharField(max_length=255)
    status_type = models.CharField(max_length=255)

    shares = models.IntegerField()
    likes = models.IntegerField()
    comments = models.IntegerField()

    objects = NewsFeedManager()

    def __str__(self):
        return ""


class NewsFeedAdmin(admin.ModelAdmin):
    list_display = ('id', 'fbid', 'message', 'story', 'created_time', 'updated_time', 'author_id', 'picture_url', 'link_url', 'link_name', 'link_description', 'link_caption', 'type', 'status_type', 'shares', 'likes', 'comments')
    '''
    def get_customer(self, obj):
        return obj.customer.nickname
    def get_translaters(self, obj):
        text = ''
        for translater in obj.translaters.all():
            text = text + translater.nickname + ', '
        return text
    '''
admin.site.register(NewsFeed, NewsFeedAdmin)