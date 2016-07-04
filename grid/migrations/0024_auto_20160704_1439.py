# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-04 19:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grid', '0023_plan_articles'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='article_type',
            field=models.CharField(choices=[('T', 'Top'), ('B', 'Bottom'), ('O', 'Outer'), ('D', 'Dress'), ('A', 'Details'), ('S', 'Shoes')], max_length=1, null=True),
        ),
    ]
