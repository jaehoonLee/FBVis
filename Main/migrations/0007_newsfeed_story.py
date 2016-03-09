# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Main', '0006_newsfeed_author_img_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='newsfeed',
            name='story',
            field=models.CharField(default='', max_length=255),
            preserve_default=False,
        ),
    ]
