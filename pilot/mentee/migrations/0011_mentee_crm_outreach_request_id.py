# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-03-11 06:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mentee', '0010_auto_20160310_1739'),
    ]

    operations = [
        migrations.AddField(
            model_name='mentee',
            name='CRM_Outreach_Request_ID',
            field=models.CharField(blank=True, max_length=80),
        ),
    ]
