# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-21 10:32
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('mentee', '0003_auto_20160121_0052'),
    ]

    operations = [
        migrations.AddField(
            model_name='mentee',
            name='Mentee_updated',
            field=models.DateTimeField(auto_now=True, default=datetime.datetime(2016, 1, 21, 10, 32, 32, 108000, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
