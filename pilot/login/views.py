from django import views
from django import forms
from django.contrib.auth import update_session_auth_hash, models
from django.contrib import messages, auth
from django.contrib.auth import models, authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, SetPasswordForm, PasswordChangeForm
from django.contrib.auth.models import User
from django.core.context_processors import csrf
from django.db.models import Count, Min, Sum, Avg
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404, redirect, render_to_response
from django.template import RequestContext
from django.views.decorators.csrf import csrf_protect
from django.views.generic import ListView
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import FormMixin, CreateView
from django.views.generic.list import ListView

import functools
import warnings

from django.conf import settings
# Avoid shadowing the login() and logout() views below.
from django.contrib.auth import (
    REDIRECT_FIELD_NAME, get_user_model, login as auth_login,
    logout as auth_logout, update_session_auth_hash,
)
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import (
    AuthenticationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm,
)
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, QueryDict
from django.shortcuts import resolve_url
from django.template.response import TemplateResponse
from django.utils.deprecation import (
    RemovedInDjango20Warning, RemovedInDjango110Warning,
)
from django.utils.encoding import force_text
from django.utils.http import is_safe_url, urlsafe_base64_decode
from django.utils.six.moves.urllib.parse import urlparse, urlunparse
from django.utils.translation import ugettext as _
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters

from config.models import Chapter, Region, UserProfile
from log.models import log
from mentee.models import Mentee

from forms import MyRegistrationForm

def deprecate_current_app(func):
    """
    Handle deprecation of the current_app parameter of the views.
    """
    @functools.wraps(func)
    def inner(*args, **kwargs):
        if 'current_app' in kwargs:
            warnings.warn(
                "Passing `current_app` as a keyword argument is deprecated. "
                "Instead the caller of `{0}` should set "
                "`request.current_app`.".format(func.__name__),
                RemovedInDjango20Warning
            )
            current_app = kwargs.pop('current_app')
            request = kwargs.get('request', None)
            if request and current_app is not None:
                request.current_app = current_app
        return func(*args, **kwargs)
    return inner
     
@csrf_protect
def login_user(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect("/mentee/")
    else:
        c = {}
        state = "Please log in below..."
        username = password = ''
        if request.POST:
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    messages.success(request, "You've been successfully logged in!")
                    up = UserProfile.objects.filter(User=user)
                    for obj in up:
                        User =  str(obj.User)
                        Chapter = str(obj.Chapter)
                        Region = str(obj.Region)
                        Perm = str(obj.Mentor_Type)
                        request.session['User'] = User
                        request.session['Chapter'] = Chapter
                        request.session['Region'] = Region
                        request.session['Perm'] = Perm
                        res_user =  request.session.get('User', default=None)
                        res_chapter =  request.session.get('Chapter', default=None)
                        res_region =  request.session.get('Region', default=None)
                        res_perm =  request.session.get('Perm', default=None)
                    state = "You've been successfully logged in!"
                    return HttpResponseRedirect('/mentee/') 
                else:
                    messages.success(request, "Your account is not active, please contact the site admin.")
                    state = "Your account is not active, please contact the site admin."
            else:
                messages.success(request, "Your username and/or password were incorrect.")
                state = "Your username and/or password were incorrect."
                
            
        
        return render_to_response('base.html',{'state':state, 'username': username}, context_instance=RequestContext(request))    

def logout_user(request):
    logout(request)
    messages.success(request, "You've been successfully logged out!")
    return HttpResponseRedirect('/') 

@sensitive_post_parameters()
@csrf_protect
@login_required
@deprecate_current_app
def passwordreset(request,
                    template_name='password_change_form.html',
                    post_change_redirect=None,
                    password_change_form=PasswordChangeForm,
                    extra_context=None):
    if post_change_redirect is None:
        post_change_redirect = reverse('password_change_done')
    else:
        post_change_redirect = resolve_url(post_change_redirect)
    if request.method == "POST":
        form = password_change_form(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            # Updating the password logs out all other sessions for the user
            # except the current one if
            # django.contrib.auth.middleware.SessionAuthenticationMiddleware
            # is enabled.
            update_session_auth_hash(request, form.user)
            return HttpResponseRedirect(post_change_redirect)
    else:
        form = password_change_form(user=request.user)
    context = {
        'form': form,
        'title': _('Password change'),
    }
    if extra_context is not None:
        context.update(extra_context)

    return TemplateResponse(request, template_name, context)
    
@login_required
@deprecate_current_app
def password_change_done(request,
                         template_name='password_change_done.html',
                         extra_context=None):
    context = {
        'title': ('Password change successful'),
    }
    if extra_context is not None:
        context.update(extra_context)

    return TemplateResponse(request, template_name, context)
    
    # template_name = 'register.html'
    # form_class = PasswordChangeForm
    # model = User
    
    # def get_form(self, form_class):
        # return form_class(user=self.request.user)
        

    # def get_object(self):
        # return User.objects.get(username=self.request.user)        
    
    # def get_success_url(self):
        # print "get_success_url"
        # print self.request.user
        # return '/'

    # def form_valid(self, form):
        # print "valid"
        # #instance = form.save(commit=False)
        # #instance.user = self.request.user
        # return super(PasswordChangeForm, self).form_valid(form)

    # def form_invalid(self,form):
        # print "form_invalid"
        # print form.errors
        # return super(PasswordChangeForm, self).form_invalid(form)           
        
       # return render_to_response('password_change_form.html')    
    
    
def register_user(request):
    if request.method == 'POST':
        c = {}
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "The account has been created!")
            #return render_to_response('base.html', args)
            return HttpResponseRedirect('/')
            
    args = {}
    args.update(csrf(request))
    
    args['form'] = MyRegistrationForm()
    
    return render_to_response('register.html', args)

    
@login_required  
def Mentor_List(request):
    if request.user.is_authenticated():
        res_user =  request.session.get('User', default=None)
        res_chapter =  request.session.get('Chapter', default=None)
        res_region =  request.session.get('Region', default=None)
        res_perm =  request.session.get('Perm', default=None)
        queryset = UserProfile.objects.all()
        if str(res_perm) == "Volunteer":
            messages.success(request, "You aren't authorized to view this record. If you feel this is in error please contact your Regional staff.")
            return render(request, "base.html")  
        
        elif str(res_perm) == "Chapter Staff":
            queryset = UserProfile.objects.filter(Chapter=res_chapter)
            for obj in UserProfile : 
                num_mentees = Mentee.Mentor_Assigned.filter(User=User).count()
            context = {
                "object_list": queryset,
                "title": "My Chapters Outreach Volunteers",
            }
            return render(request, "mentor_list.html",context)
        
        elif str(res_perm) == "Regional Staff":
            all_logs = log.objects.all()[0]
            queryset = UserProfile.objects.filter(Region=res_region).annotate(num_logs=Count('log'), num_mentees=Count('mentee'))
            context = {
                "object_list": queryset,
                "title": "My Regions Outreach Volunteers"
            }
            return render(request, "mentor_list.html",context)
            
        elif str(res_perm) == "National Staff":
            queryset = UserProfile.objects.all()
            context = {
                "object_list": queryset,
                "title": "All Outreach Volunteers"
            }   
            return render(request, "mentor_list.html",context) 
        
        else:
            messages.success(request, "You aren't authorized to view this record. If you feel this is in error please contact your chapter staff.")
            return render(request, "base.html")
    else:
        messages.success(request, "Please log in to view that page")
        return render(request, "base.html")
        
@login_required  
def Mentor_Table(request): 
    if request.user.is_authenticated():
        res_user =  request.session.get('User', default=None)
        res_chapter =  request.session.get('Chapter', default=None)
        res_region =  request.session.get('Region', default=None)
        res_perm =  request.session.get('Perm', default=None)
        queryset = UserProfile.objects.all()
        if str(res_perm) == "Volunteer":
            messages.success(request, "You aren't authorized to view this record. If you feel this is in error please contact your Regional staff.")
            return render(request, "base.html")  
        
        elif str(res_perm) == "Chapter Staff":
            queryset = UserProfile.objects.filter(Chapter=res_chapter)
            for obj in UserProfile : 
                num_mentees = Mentee.Mentor_Assigned.filter(User=User).count()
                print queryset.values()
            context = {
                "object_list": queryset,
                "title": "My Chapters Outreach Volunteers",
            }
            return render(request, "mentor_table.html",context)
        
        elif str(res_perm) == "Regional Staff":
            all_logs = log.objects.all()[0]
            queryset = UserProfile.objects.filter(Region=res_region).annotate(num_logs=Count('log'), num_mentees=Count('mentee'))
            context = {
                "object_list": queryset,
                "title": "My Regions Outreach Volunteers"
            }
            return render(request, "mentor_table.html",context)
            
        elif str(res_perm) == "National Staff":
            queryset = UserProfile.objects.filter(Mentor_Assigned=user)
            context = {
                "object_list": queryset,
                "title": "All Outreach Volunteers"
            }   
            return render(request, "mentor_table.html",context) 
        
        else:
            messages.success(request, "You aren't authorized to view this record. If you feel this is in error please contact your chapter staff.")
            return render(request, "base.html")
    else:
        messages.success(request, "Please log in to view that page")
        return render(request, "base.html")


@login_required        
def mentor_detail(request, id=None):
    res_user =  request.session.get('User', default=None)
    res_chapter =  request.session.get('Chapter', default=None)
    res_region =  request.session.get('Region', default=None)
    res_perm =  request.session.get('Perm', default=None)
    if request.user.is_authenticated():    
        instance = get_object_or_404(UserProfile, id=id)
        upid=instance.User
        user_addon = auth.models.User.objects.filter(username=upid)
        instance_log = Mentee.objects.filter(Mentor_Assigned=instance.id).annotate(num_mentee=Count('log'))
        context = {
            "title": instance.User_Full_Name,
            "instance": instance,
            "user_addon": user_addon,
            "instance_log": instance_log,
        }
        if str(res_perm) == "Volunteer":
            if str(instance.Mentor_Assigned) == res_user:
                return render(request, "mentor_detail.html",context)    
            else:
                messages.success(request, "You aren't authorized to view this record. If you feel this is in error please contact your chapter staff.")
                return render(request, "base.html")                        
        elif str(res_perm) == "Chapter Staff":
            if str(instance.Chapter) == res_chapter:
                return render(request, "mentor_detail.html",context)
            else:
                messages.success(request, "You aren't authorized to view this record. If you feel this is in error please contact your Regional staff.")
                return render(request, "base.html")                        
        elif str(res_perm) == "Regional Staff":
            if str(instance.Region) == str(res_region):
                return render(request, "mentor_detail.html",context)  
            else:
                messages.success(request, "You aren't authorized to view this record. If you feel this is in error please contact your National staff.")
                return render(request, "base.html")        
        elif str(res_perm) == "National Staff":            
            return render(request, "mentor_detail.html",context)
           
    else:
        context = {
            "title": "Please Log In"
        }
        return render(request, "base.html",context)          
