from django import forms
from .models import Mentee
from django.contrib.admin import widgets

class MenteeForm(forms.ModelForm):
    #Diagnosis_Date = forms.DateField(widget=forms.SelectDateWidget(empty_label="Nothing"))
    class Meta:
        model = Mentee
        exclude = [
            "Created_By",
            "timestamp",
            "updated",
            "Updated_By",
        ]
