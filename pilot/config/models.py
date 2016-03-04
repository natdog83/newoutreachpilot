from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from django.db import models

class Region(models.Model):
    Region_Name = models.CharField(max_length=80, primary_key=True)
    Region_Created_By = models.ForeignKey(User)

    def __unicode__(self):
        return self.Region_Name

class Chapter(models.Model):
    Chapter_Name = models.CharField(max_length=80, primary_key=True)
    Chapter_Regoin = models.ForeignKey(Region)
    Chapter_Created_By = models.ForeignKey(User)

    def __unicode__(self):
        return self.Chapter_Name

class outreach_permision(models.Model):
    Permision_Type = models.CharField(max_length=80)

    def __unicode__(self):
        return self.Permision_Type

class UserProfile(models.Model):
    User = models.OneToOneField(User, on_delete=models.CASCADE)
    User_Full_Name = models.CharField(max_length=80, blank=True)
    User_Phone_Number = models.CharField(max_length=80, blank=True)
    Chapter = models.ForeignKey(Chapter)
    Region = models.ForeignKey(Region)
    Mentor_Type = models.ForeignKey(outreach_permision)
    def user_email(self):
        return self.User.email

    def __unicode__(self):
        return str(self.User)


    def get_absolute_url(self):
        return reverse('mentor_detail', kwargs={"id": self.id})
