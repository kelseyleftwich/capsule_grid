# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-04 21:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grid', '0024_auto_20160704_1439'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plan',
            name='articles',
            field=models.ManyToManyField(blank=True, to='grid.Article'),
        ),
    ]