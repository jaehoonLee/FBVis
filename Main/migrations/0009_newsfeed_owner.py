# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Main', '0008_auto_20160919_2213'),
    ]

    operations = [
        migrations.AddField(
            model_name='newsfeed',
            name='owner',
            field=models.ForeignKey(null=True, to=settings.AUTH_USER_MODEL, unique=True),
        ),
    ]
