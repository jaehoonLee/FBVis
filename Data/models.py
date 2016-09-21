from django.db import models
from django.contrib import admin

# Create your models here.
class FacebookFriendManager(models.Manager):
    def create_facebookfriend(self, name, fbid, img_url, close):
        facebookfriend = self.model(name=name, fbid=fbid, img_url=img_url, close=close)
        facebookfriend.save()
        return facebookfriend


class FacebookFriend(models.Model):
    name = models.CharField(max_length=255)
    fbid = models.CharField(max_length=255, unique=True)
    img_url = models.CharField(max_length=255)
    close = models.BooleanField()

    objects = FacebookFriendManager()

class FacebookFriendAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'fbid', 'img_url', 'close')

admin.site.register(FacebookFriend, FacebookFriendAdmin)




