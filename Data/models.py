from django.db import models
from django.contrib import admin

# Create your models here.
class FacebookFriendManager(models.Manager):
    def create_facebookfriend(self, name, fbid, close):
        facebookfriend = self.model(name=name, fbid=fbid, close=close)
        facebookfriend.save()
        return facebookfriend


class FacebookFriend(models.Model):
    name = models.CharField(max_length=255, unique=True)
    fbid = models.CharField(max_length=255, unique=True)
    close = models.BooleanField()

    objects = FacebookFriendManager()

class FacebookFriendAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'fbid', 'close')

admin.site.register(FacebookFriend, FacebookFriendAdmin)




