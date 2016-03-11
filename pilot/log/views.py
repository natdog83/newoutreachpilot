from datetime import datetime
import json
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Count, Min, Sum, Avg
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.edit import FormMixin, CreateView
from django.views.generic.list import ListView
from django import views
from config.models import Chapter, Region, UserProfile
from log.models import log
from .models import Mentee
from .forms import LogForm

@login_required
def logtable(request):
    if request.user.is_authenticated():
        user = request.user
        res_user =  request.session.get('User', default=None)
        res_chapter =  request.session.get('Chapter', default=None)
        res_region =  request.session.get('Region', default=None)
        res_perm =  request.session.get('Perm', default=None)
        mentor = UserProfile.objects.filter(User=user)
        if str(res_perm) == "Volunteer":
            instance_log = log.objects.filter(Log_User=mentor).order_by('-timestamp')
            context = {
                "instance_log": instance_log,
                "title": "My Activities",

            }
            return render(request, "log_table.html",context)

        elif str(res_perm) == "Chapter Staff":
            instance_log = log.objects.filter(Log_Chapter=res_chapter).order_by('-timestamp')
            context = {
                "instance_log": instance_log,
                "title": "My Chapters Activities"
            }
            return render(request, "log_table.html",context)

        elif str(res_perm) == "Regional Staff":
            instance_log = log.objects.filter(Log_Region=res_region).order_by('-timestamp')
            context = {
                "instance_log": instance_log,
                "title": "My Regions Activities"
            }
            return render(request, "log_table.html",context)

        elif str(res_perm) == "National Staff":
            instance_log = log.objects.all.order_by('-timestamp')
            context = {
                "instance_log": instance_log,
                "title": "All Activities"
            }
            return render(request, "log_table.html",context)

        else:
            messages.success(request, "You aren't authorized to view this record. If you feel this is in error please contact your chapter staff.")
            return render(request, "base.html")
    else:
        messages.success(request, "Please log in to view that page")
        return render(request, "base.html")

@login_required
def Log_Create_Form(request):
    user = request.user
    res_user =  request.session.get('User')
    res_chapter =  request.session.get('Chapter')
    res_region =  request.session.get('Region')
    res_perm =  request.session.get('Perm')
    form = LogForm(request.POST)
    mentor = UserProfile.objects.filter(User=user)
    #currentuser = UserProfile.objects.filter(User=user).values
    #form = LogForm(request.POST, instance=request.user)
    if str(res_perm) == "Volunteer":
        form.fields['Outreach_Family'].queryset = Mentee.objects.filter(Mentor_Assigned=mentor)
        form.fields['Log_User'].queryset = UserProfile.objects.filter(User=user)
    if str(res_perm) == "Chapter Staff":
        form.fields['Outreach_Family'].queryset = Mentee.objects.filter(Chapter=res_chapter)
        form.fields['Log_User'].queryset = UserProfile.objects.filter(User=user)
    if str(res_perm) == "Regional Staff":
        form.fields['Outreach_Family'].queryset = Mentee.objects.filter(Region=res_region)
        form.fields['Log_User'].queryset = UserProfile.objects.filter(User=user)

    context = {
        "form": form,
    }
    if request.POST:
        if form.is_valid():
            instance = form.save(commit=False)
            #instance.Log_User = request.User
            instance.timestamp = datetime.now()
            instance.Log_Chapter = res_chapter
            instance.Log_Region = res_region
            #instance.Log_User = currentuser
            instance.save()
            messages.success(request or None, "Saved")
            #return render(request, "Log_Form.html", context)
            return HttpResponseRedirect('/activities/', instance.id)

    else:
        messages.success(request or None, "Not Saved")
        return render(request, "Log_Form.html", context)

@login_required
def log_details(request, id=None):
    res_user =  request.session.get('User', default=None)
    res_chapter =  request.session.get('Chapter', default=None)
    res_region =  request.session.get('Region', default=None)
    res_perm =  request.session.get('Perm', default=None)
    if request.user.is_authenticated():
        instance = get_object_or_404(log, id=id)
        context = {
            "title": instance.Outreach_Family,
            "instance": instance,
        }
        return render(request, "Log_Detail.html", context)
    # if str(res_perm) == "Volunteer":
        # form.fields['Outreach_Family'].queryset = Mentee.objects.filter(Mentor_Assigned=res_user)
    # if str(res_perm) == "Chapter Staff":
        # form.fields['Outreach_Family'].queryset = Mentee.objects.filter(Chapter=res_chapter)
    # if str(res_perm) == "Regional Staff":
        # form.fields['Outreach_Family'].queryset = Mentee.objects.filter(Region=res_region)


    # else:
        # messages.success(request or None, "Not Saved")
        # return render(request, "Log_Form.html", context)
