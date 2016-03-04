from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from config.models import UserProfile, Region, Chapter

class MyRegistrationForm(UserCreationForm):
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email',)
        
    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        
        if commit:
            user.save()
            

        return user