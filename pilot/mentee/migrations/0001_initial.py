# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-20 07:38
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('config', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Mentee',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Mentee_Name', models.CharField(max_length=80)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('Mentee_Created_By', models.CharField(max_length=80)),
                ('Mentee_Chapter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='config.Chapter')),
                ('Mentee_Region', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='config.Region')),
                ('Mentor_Assigned', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
