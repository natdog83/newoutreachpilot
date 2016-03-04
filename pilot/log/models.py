from __future__ import unicode_literals
from datetime import datetime
from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from mentee.models import Mentee
from config.models import UserProfile

class log(models.Model):
    PHONE = 'Phone call'
    EMAIL = 'E-Mail'
    MEETING = 'In-Person Meeting'
    USPS = 'USPS Mailing'
    BAGOFHOPE = 'Bag of Hope'
    CHAPTERACTIVITY = 'Chapter Outreach activity/event information'
    EADULTTOOLKIT = 'Experienced Adult Toolkit'
    NDADULTTOOLKIT = 'Newly Diagnosed Adult Toolkit'
    OWKICKOFF = 'One Walk Kickoff Information/Invitation'
    OWINFORMATION = 'One Walk information/Invitation'
    PREGNANCYTOOLKIT = 'Pregnancy Toolkit'
    SOCIALMEDIA = "Social Media"
    SCHOOLADVISORYTOOLKIT = 'School Advisory Toolkit'
    T1DCAREKIT = 'T1D Care Kit'
    TEENTOOLKIT = 'Teen Toolkit'
    TRIALNETBROCURE = 'TrialNet Brochure'
    TYPEONENATIONSUMMIT = 'TypeOneNation Summit Information/Invitation'
    OTHER = 'Other (in notes section provide details)'
    TYPECHOICES = [
        (PHONE, 'Phone call'),
        (EMAIL, 'E-Mail'),
        (MEETING, 'In-Person Meeting'),
        (SOCIALMEDIA, 'Social Media'),
        (USPS, 'USPS Mailing'),
    ]
    JDRFRESOURCECHOICES = [
        (BAGOFHOPE, 'Bag of Hope'),
        (CHAPTERACTIVITY, 'Chapter Outreach activity/event information'),
        (EADULTTOOLKIT, 'Experienced Adult Toolkit'),
        (NDADULTTOOLKIT, 'Newly Diagnosed Adult Toolkit'),
        (OWKICKOFF, 'One Walk Kickoff Information/Invitation'),
        (OWINFORMATION, 'One Walk information/Invitation'),
        (PREGNANCYTOOLKIT, 'Pregnancy Toolkit'),
        (SCHOOLADVISORYTOOLKIT, 'School Advisory Toolkit'),
        (T1DCAREKIT, 'T1D Care Kit'),
        (TEENTOOLKIT, 'Teen Toolkit'),
        (TRIALNETBROCURE, 'TrialNet Brochure'),
        (TYPEONENATIONSUMMIT, 'TypeOneNation Summit Information/Invitation'),
        (OTHER, 'Other (in notes section provide details)'),
    ]
    Activity_Date = models.DateField()
    Outreach_Family = models.ForeignKey(Mentee)
    Log_Method = models.CharField(max_length=80, choices=TYPECHOICES, blank=True)
    JDRF_Resource_Sent = models.CharField(max_length=80, choices=JDRFRESOURCECHOICES, blank=True)
    Log_Notes = models.TextField(blank=True)
    Log_User = models.ForeignKey(UserProfile)
    Log_Chapter = models.CharField(max_length=80, blank=True)
    Log_Region = models.CharField(max_length=80, blank=True)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    def get_absolute_url(self):
        return reverse('log_detail', kwargs={"id": self.id})
