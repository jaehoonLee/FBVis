# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Main', '0005_remove_newsfeed_author_img_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='newsfeed',
            name='author_img_url',
            field=models.CharField(default='', max_length=255),
            preserve_default=False,
        ),
    ]
