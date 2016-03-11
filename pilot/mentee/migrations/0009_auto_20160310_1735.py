# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-03-11 01:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mentee', '0008_auto_20160310_1724'),
    ]

    operations = [
        migrations.RenameField(
            model_name='mentee',
            old_name='Phone_Number',
            new_name='Home_Number',
        ),
        migrations.AddField(
            model_name='mentee',
            name='Business_Number',
            field=models.CharField(blank=True, max_length=25),
        ),
        migrations.AddField(
            model_name='mentee',
            name='City',
            field=models.CharField(blank=True, max_length=80),
        ),
        migrations.AddField(
            model_name='mentee',
            name='Employer',
            field=models.CharField(blank=True, max_length=80),
        ),
        migrations.AddField(
            model_name='mentee',
            name='Endo',
            field=models.CharField(blank=True, max_length=80),
        ),
        migrations.AddField(
            model_name='mentee',
            name='Gender',
            field=models.CharField(blank=True, choices=[('Male', 'Male'), ('Female', 'Female')], max_length=80),
        ),
        migrations.AddField(
            model_name='mentee',
            name='Grade',
            field=models.CharField(blank=True, max_length=80),
        ),
        migrations.AddField(
            model_name='mentee',
            name='Has_Diabetes',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='mentee',
            name='LastName',
            field=models.CharField(blank=True, max_length=80),
        ),
        migrations.AddField(
            model_name='mentee',
            name='Mailing_Address_Line_2',
            field=models.CharField(blank=True, max_length=80),
        ),
        migrations.AddField(
            model_name='mentee',
            name='Mailing_Address_Line_3',
            field=models.CharField(blank=True, max_length=80),
        ),
        migrations.AddField(
            model_name='mentee',
            name='Mobile_Phone',
            field=models.CharField(blank=True, max_length=15),
        ),
        migrations.AddField(
            model_name='mentee',
            name='Preferred_Phone',
            field=models.CharField(blank=True, choices=[('Home Phone', 'Home Phone'), ('Business Phone', 'Business Phone'), ('Mobile Phone', 'Mobile Phone')], max_length=80),
        ),
        migrations.AddField(
            model_name='mentee',
            name='State',
            field=models.CharField(blank=True, max_length=80),
        ),
        migrations.AddField(
            model_name='mentee',
            name='Zip',
            field=models.CharField(blank=True, max_length=80),
        ),
    ]
