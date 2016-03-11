from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from config.models import Chapter, Region, UserProfile

class Mentee(models.Model):
    MALE = 'Male'
    FEMALE = 'Female'
    SEX = [
        (MALE, 'Male'),
        (FEMALE, 'Female',)
    ]
    Name = models.CharField(max_length=80)
    CRM_Record_ID = models.CharField(max_length=80, blank=True)
    Email = models.EmailField(blank=True)
    Address = models.CharField(max_length=80, blank=True)
    Phone_Number = models.CharField(max_length=15, blank=True)
    Child_T1D_name = models.CharField(max_length=80, blank=True)
    Child_Gender = models.CharField(max_length=80, choices=SEX, blank=True)
    Childs_Age = models.CharField(max_length=80, blank=True)
    Diagnosis_Date =  models.DateField(auto_now=False, auto_now_add=False, blank=True)
    Hospital_Endo = models.CharField(max_length=80, blank=True)
    School_Grade = models.CharField(max_length=80, blank=True)
    Chapter = models.ForeignKey(Chapter)
    Region = models.ForeignKey(Region)
    Mentor_Assigned = models.ForeignKey(UserProfile)
    Notes = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    Created_By = models.CharField(max_length=80, blank=True)
    Updated_By = models.CharField(max_length=80, blank=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    
    def __unicode__(self):
        return self.Name
        
    def get_absolute_url(self):
        return reverse('mentee_detail', kwargs={"id": self.id})