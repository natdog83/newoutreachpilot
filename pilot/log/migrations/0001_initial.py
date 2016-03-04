# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-21 19:36
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mentee', '0004_mentee_mentee_updated'),
    ]

    operations = [
        migrations.CreateModel(
            name='log',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Log_Date', models.DateField()),
                ('Log_Method', models.CharField(blank=True, choices=[('Phone call', 'Phone call'), ('E-Mail', 'E-Mail'), ('In-Person Meeting', 'In-Person Meeting')], max_length=80)),
                ('Log_Notes', models.TextField(blank=True)),
                ('Log_Chapter', models.CharField(blank=True, max_length=80)),
                ('Log_Region', models.CharField(blank=True, max_length=80)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('Log_Mentee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mentee.Mentee')),
                ('Log_User', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]