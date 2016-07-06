# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grid', '0027_auto_20160706_1620'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='image_slurp',
            field=models.URLField(null=True),
        ),
    ]
