# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grid', '0030_auto_20160710_1249'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='to_make',
            field=models.BooleanField(choices=[(False, 'No'), (True, 'Yes')], default=False),
        ),
        migrations.AddField(
            model_name='article',
            name='to_purchase',
            field=models.BooleanField(choices=[(False, 'No'), (True, 'Yes')], default=False),
        ),
    ]
