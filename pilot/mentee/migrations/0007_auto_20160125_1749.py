# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-26 01:49
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mentee', '0006_mentee_crm_record_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mentee',
            name='Mentor_Assigned',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='config.UserProfile'),
        ),
    ]
