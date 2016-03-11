from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from config.models import Chapter, Region, UserProfile

class Mentee(models.Model):
    MALE = 'Male'
    FEMALE = 'Female'
    HOMEPHONE = 'Home Phone'
    BUSINESSPHONE = 'Business Phone'
    MOBILEPHONE = 'Mobile Phone'
    PHONE = [
        (HOMEPHONE, 'Home Phone'),
        (BUSINESSPHONE, 'Business Phone'),
        (MOBILEPHONE, 'Mobile Phone'),
    ]
    SEX = [
        (MALE, 'Male'),
        (FEMALE, 'Female',)
    ]
    CRM_Record_ID = models.CharField(max_length=80, blank=True)
    CRM_Outreach_Request_ID = models.CharField(max_length=80, blank=True)
    First_Name = models.CharField(max_length=80)
    Last_Name = models.CharField(max_length=80, blank=True)
    Gender = models.CharField(max_length=80, choices=SEX, blank=True)
    Mailing_Address_Line_1 = models.CharField(max_length=80, blank=True)
    Mailing_Address_Line_2 = models.CharField(max_length=80, blank=True)
    Mailing_Address_Line_3 = models.CharField(max_length=80, blank=True)
    City = models.CharField(max_length=80, blank=True)
    State = models.CharField(max_length=80, blank=True)
    Zip = models.CharField(max_length=80, blank=True)
    Preferred_Phone = models.CharField(max_length=80, choices=PHONE, blank=True)
    Home_Number = models.CharField(max_length=15, blank=True)
    Business_Number = models.CharField(max_length=25, blank=True)
    Mobile_Phone = models.CharField(max_length=15, blank=True)
    Email = models.EmailField(blank=True)
    Employer = models.CharField(max_length=80, blank=True)
    Has_Diabetes = models.BooleanField(default=False)
    Child_T1D_name = models.CharField(max_length=80, blank=True)
    Child_Gender = models.CharField(max_length=80, choices=SEX, blank=True)
    Childs_DOB = models.DateField(auto_now=False, auto_now_add=False, blank=True)
    Diagnosis_Date =  models.DateField(auto_now=False, auto_now_add=False, blank=True)
    Hospital = models.CharField(max_length=80, blank=True)
    Endo = models.CharField(max_length=80, blank=True)
    School = models.CharField(max_length=80, blank=True)
    Grade = models.CharField(max_length=80, blank=True)
    Chapter = models.ForeignKey(Chapter)
    Region = models.ForeignKey(Region)
    Mentor_Assigned = models.ForeignKey(UserProfile)
    Notes = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    Created_By = models.CharField(max_length=80, blank=True)
    Updated_By = models.CharField(max_length=80, blank=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __unicode__(self):
        return self.First_Name + ' ' + self.Last_Name

    def get_absolute_url(self):
        return reverse('mentee_detail', kwargs={"id": self.id})
