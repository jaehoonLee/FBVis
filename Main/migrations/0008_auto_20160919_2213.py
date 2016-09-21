# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Main', '0007_newsfeed_story'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='newsfeed',
            name='author',
        ),
        migrations.RemoveField(
            model_name='newsfeed',
            name='author_img_url',
        ),
    ]
