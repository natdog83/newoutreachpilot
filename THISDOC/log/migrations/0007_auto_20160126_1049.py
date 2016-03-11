# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-26 18:49
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('log', '0006_log_jdrf_resource_sent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='log',
            name='Log_User',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]