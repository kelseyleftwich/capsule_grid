# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-30 00:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grid', '0004_auto_20160629_1842'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='article_type',
            field=models.CharField(choices=[('T', 'Top'), ('B', 'Bottom'), ('D', 'Details')], max_length=1, null=True),
        ),
    ]