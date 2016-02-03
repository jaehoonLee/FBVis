# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='NewsFeed',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fbid', models.CharField(unique=True, max_length=255)),
                ('created_time', models.DateTimeField()),
                ('updated_time', models.DateTimeField()),
                ('author', models.CharField(max_length=255)),
                ('author_id', models.CharField(max_length=255)),
                ('message', models.TextField()),
                ('picture_url', models.TextField()),
                ('link_url', models.TextField()),
                ('link_name', models.TextField()),
                ('link_description', models.TextField()),
                ('link_caption', models.TextField()),
                ('type', models.CharField(max_length=255)),
                ('status_type', models.CharField(max_length=255)),
                ('shares', models.IntegerField()),
                ('likes', models.IntegerField()),
                ('comments', models.IntegerField()),
            ],
        ),
    ]
