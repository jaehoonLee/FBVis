# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Data', '0002_facebookfriend_img_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='facebookfriend',
            name='name',
            field=models.CharField(max_length=255),
        ),
    ]
