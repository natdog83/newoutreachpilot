
from django import forms
from django.forms.widgets import Select
from config.models import UserProfile, Chapter
from config import models
from mentee.models import Mentee
from .models import log

class LogForm(forms.ModelForm):
    # def __init__(self, user=None, **kwargs):
    #super(LogForm, self).__init__(**kwargs)
    # res_user =  UserProfile.objects.get(User=user).User
    # res_chapter =  str(UserProfile.objects.get(User=user).Chapter)
    # res_region =  UserProfile.objects.get(User=user).Region
    # res_perm =  UserProfile.objects.get(User=user).Mentor_Type


    Activity_Date = forms.DateField(widget=forms.SelectDateWidget(empty_label="Nothing"))
    
    class Meta:
        model = log
        exclude = [
            "timestamp",
            "Log_Region",
            "Log_Chapter",
            #"Log_User",
        ]
        widgets = {
            'Log_Chapter': Select(),
        }

            

            