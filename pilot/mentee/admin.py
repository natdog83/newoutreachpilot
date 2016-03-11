from .models import Mentee
from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class MenteeAdmin(admin.ModelAdmin):
    fields= (
        'CRM_Record_ID',
        'First_Name',
        'Last_Name',
        'Gender',
        'Mailing_Address_Line_1',
        'Mailing_Address_Line_2',
        'Mailing_Address_Line_3',
        'City',
        'State',
        'Zip',
        'Preferred_Phone',
        'Home_Number',
        'Business_Number',
        'Mobile_Phone',
        'Email',
        'Employer',
        'Has_Diabetes',
        'Child_T1D_name',
        'Child_Gender',
        'Childs_DOB',
        'Diagnosis_Date',
        'Hospital',
        'Endo',
        'School',
        'Grade',
        'Chapter',
        'Region',
        'Mentor_Assigned',
        'Notes',
    )
    list_display = ('__unicode__', 'Chapter', 'Mentor_Assigned',)

    def save_model(self, request, obj, form, change):
        obj.Updated_By = str(request.user)
        obj.save()

    def save_formset(self, request, form, formset, change):
        if formset.model == Mentee:
            instances = formset.save(commit=False)
            for instance in instances:
                instance.Updated_By = str(request.user)
                instance.save()
        else:
            formset.save()

admin.site.register(Mentee, MenteeAdmin)
