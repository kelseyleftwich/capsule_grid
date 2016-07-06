# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grid', '0026_auto_20160704_1624'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plan',
            name='articles',
            field=models.ManyToManyField(blank=True, to='grid.Article'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='profile_type',
            field=models.CharField(choices=[('F', 'Free'), ('P', 'Paid')], default='P', max_length=1),
        ),
    ]
