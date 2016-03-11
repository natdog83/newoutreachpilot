from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Chapter, Region, UserProfile, outreach_permision, UserProfile

from django import forms

class RegionListView(admin.ModelAdmin):
    list_display = ["__unicode__"]
    class Meta:
        model = Region
        fields = ["Region_Name"]
    
    def saveform(self):  
        user = request.User
        if form.is_valid():
            instance = form.save(commit=False)
            instance.Region_Created_By = user
            instance.save()
            
            return obj.Region_Name  

class ChapterListView(admin.ModelAdmin):
    list_display = ["__unicode__"]
    class Meta:
        model = Chapter
        fields = ("Chapter_Name", "Region_Name")
    
    def saveform(self):    
        user = request.User
        if form.is_valid():
            instance = form.save(commit=False)
            instance.Chapter_Created_By = ser
            instance.save()
            
            return obj.Chapter_Name  

class UserInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'User'

class UserAdmin(BaseUserAdmin):
    inlines = (UserInline, )
    
class UserCreateForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('first_name' , 'last_name', 'email', 'is_staff',)


class UserAdmin(UserAdmin):
    add_form = UserCreateForm
    prepopulated_fields = {'username': ('first_name', 'last_name'),}

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('first_name', 'last_name',  'email', 'username', 'password1', 'password2', 'is_staff',),
        }),
    )   

class UserProfileForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        exclude = []

class UserProfileFormAdmin(admin.ModelAdmin):
    exclude = []
    form = UserProfileForm  

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)            

admin.site.register(Chapter, ChapterListView)
admin.site.register(Region, RegionListView)
admin.site.register(outreach_permision)

