# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-03 14:53
from __future__ import unicode_literals

from django.db import migrations, models
import grid.models


class Migration(migrations.Migration):

    dependencies = [
        ('grid', '0020_auto_20160703_0952'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=grid.models.get_image_path),
        ),
    ]
