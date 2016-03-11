from datetime import datetime
import json
from django import views
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import models
from django.db.models import Count, Min, Sum, Avg
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import FormMixin, CreateView
from django.views.generic.list import ListView

from config.models import Chapter, Region, UserProfile
from log.models import log
from .forms import MenteeForm
from .models import Mentee
from log.models import log


def mentee_home(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect("mentee/")
    else:
        context = {
            "title": User
        }
        return render(request, "base.html",context)

@login_required
def mentee_list(request):
    if request.user.is_authenticated():
        user = request.user
        res_user =  request.session.get('User', default=None)
        res_chapter =  request.session.get('Chapter', default=None)
        res_region =  request.session.get('Region', default=None)
        res_perm =  request.session.get('Perm', default=None)
        mentor = UserProfile.objects.filter(User=user)
        if str(res_perm) == "Volunteer":
            queryset = Mentee.objects.filter(Mentor_Assigned=mentor).annotate(Count('log'))
            if not queryset:
                context = {
                    "title": "No Newly Diagnosed Families",
                }
                return render(request, "mentee_list.html", context)
            else:
                context = {
                    "object_list": queryset,
                    "title": "My Newly Diagnosed Families",
                }
                return render(request, "mentee_list.html",context)

        elif str(res_perm) == "Chapter Staff":
            queryset = Mentee.objects.filter(Chapter=res_chapter).annotate(Count('log'))
            context = {
                "object_list": queryset,
                "title": "My Chapters Newly Diagnosed Families"
            }
            return render(request, "mentee_list.html",context)

        elif str(res_perm) == "Regional Staff":
            all_logs = log.objects.all()[0]
            queryset = Mentee.objects.filter(Region=res_region).annotate(Count('log'), Avg('log'))
            context = {
                "object_list": queryset,
                "title": "My Regions Newly Diagnosed Families"
            }
            return render(request, "mentee_list.html",context)

        elif str(res_perm) == "National Staff":
            queryset = Mentee.objects.all().annotate(Count('log'), Avg('log'))
            context = {
                "object_list": queryset,
                "title": "All Newly Diagnosed Families"
            }
            return render(request, "mentee_list.html",context)

        else:
            messages.success(request, "You aren't authorized to view this record. If you feel this is in error please contact your chapter staff.")
            return render(request, "base.html")
    else:
        messages.success(request, "Please log in to view that page")
        return render(request, "base.html")

@login_required
def mentee_detail(request, id=None):
    res_user =  request.session.get('User', default=None)
    res_chapter =  request.session.get('Chapter', default=None)
    res_region =  request.session.get('Region', default=None)
    res_perm =  request.session.get('Perm', default=None)
    if request.user.is_authenticated():
        instance = get_object_or_404(Mentee, id=id)
        instance_log = log.objects.filter(Outreach_Family=instance.id).order_by('-timestamp')
        context = {
            "title": instance.First_Name + ' ' + instance.Last_Name,
            "instance": instance,
            "instance_log": instance_log,
        }
        if str(res_perm) == "Volunteer":
            if str(instance.Mentor_Assigned) == res_user:
                return render(request, "mentee_detail.html",context)
            else:
                messages.success(request, "You aren't authorized to view this record. If you feel this is in error please contact your chapter staff.")
                return render(request, "base.html")
        elif str(res_perm) == "Chapter Staff":
            if str(instance.Chapter) == res_chapter:
                return render(request, "mentee_detail.html",context)
            else:
                messages.success(request, "You aren't authorized to view this record. If you feel this is in error please contact your Regional staff.")
                return render(request, "base.html")
        elif str(res_perm) == "Regional Staff":
            if str(instance.Region) == str(res_region):
                return render(request, "mentee_detail.html",context)
            else:
                messages.success(request, "You aren't authorized to view this record. If you feel this is in error please contact your National staff.")
                return render(request, "base.html")
        elif str(res_perm) == "National Staff":
            return render(request, "mentee_detail.html",context)

    else:
        context = {
            "title": "Please Log In"
        }
        return render(request, "base.html",context)




@login_required
def mentee_update(request, id=None):
    if request.user.is_authenticated():
        user = request.user
        res_user =  request.session.get('User', default=None)
        res_chapter =  request.session.get('Chapter', default=None)
        res_region =  request.session.get('Region', default=None)
        res_perm =  request.session.get('Perm', default=None)
        instance = get_object_or_404(Mentee, id=id)
        form = MenteeForm(request.POST or None, instance=instance)
        mentor = UserProfile.objects.filter(User=user)

        #Permision check - Is Volunteer
        if str(res_perm) == "Volunteer":
            if str(instance.Mentor_Assigned) == res_user:
                form.fields['Mentor_Assigned'].queryset = User.objects.filter(username=mentor)
                form.fields['Chapter'].queryset = Chapter.objects.filter(Chapter_Name=res_chapter)
                form.fields['Region'].queryset = Region.objects.filter(Region_Name=res_region)
                if form.is_valid():
                    instance = form.save(commit=False)
                    instance.Updated_By = res_user
                    instance.updated = datetime.now()
                    instance.save()
                    messages.success(request or None, "Saved")
                    return HttpResponseRedirect(instance.get_absolute_url())
                else:
                    messages.error(request or None, "Not Successfully Updated")
                context = {
                    "title": instance.First_Name + ' ' + instance.Last_Name,
                    "instance": instance,
                    "form": form,
                }
                return render(request, "mentee_form.html",context)
            else:
                messages.success(request, "You aren't authorized to view this record. If you feel this is in error please contact your chapter staff.")
                return render(request, "base.html")

        #Permision check - Is chapter staff
        elif str(res_perm) == "Chapter Staff":
            if str(instance.Chapter) == res_chapter:
                form.fields['Mentor_Assigned'].queryset = UserProfile.objects.filter(Chapter=res_chapter)
                form.fields['Chapter'].queryset = Chapter.objects.filter(Chapter_Name=res_chapter)
                form.fields['Region'].queryset = Region.objects.filter(Region_Name=res_region)
                if form.is_valid():
                    instance = form.save(commit=False)
                    instance.Updated_By = res_user
                    instance.updated = datetime.now()
                    instance.save()
                    messages.success(request or None, "Saved")
                    return HttpResponseRedirect(instance.get_absolute_url())
                else:
                    messages.error(request or None, "Not Successfully Updated")
                context = {
                    "title": instance.First_Name + ' ' + instance.Last_Name,
                    "instance": instance,
                    "form": form,
                }
                return render(request, "mentee_form.html",context)
            else:
                messages.success(request, "You aren't authorized to view this record. If you feel this is in error please contact your Regional staff.")
                return render(request, "base.html")


        #Permision check - Is Regional staff
        elif str(res_perm) == "Regional Staff":
            if str(instance.Region) == str(res_region):
                form.fields['Mentor_Assigned'].queryset = UserProfile.objects.filter(Region=res_region)
                form.fields['Chapter'].queryset = Chapter.objects.filter(Chapter_Regoin=res_region)
                form.fields['Region'].queryset = Region.objects.filter(Region_Name=res_region)
                if form.is_valid():
                    instance = form.save(commit=False)
                    instance.Updated_By = res_user
                    instance.updated = datetime.now()
                    instance.save()
                    messages.success(request or None, "Saved")
                    return HttpResponseRedirect(instance.get_absolute_url())
                else:
                    messages.error(request or None, "Not Successfully Updated")
                context = {
                    "title": instance.First_Name + ' ' + instance.Last_Name,
                    "instance": instance,
                    "form": form,
                }
                return render(request, "mentee_form.html",context)
            else:
                messages.success(request, "You aren't authorized to view this record. If you feel this is in error please contact your Regional staff.")
                return render(request, "base.html")

        elif str(res_perm) == "National Staff":
            if form.is_valid():
                instance = form.save(commit=False)
                instance.Updated_By = res_user
                instance.updated = datetime.now()
                instance.save()
                messages.success(request or None, "Saved")
                return HttpResponseRedirect(instance.get_absolute_url())
            else:
                messages.error(request or None, "Not Successfully Updated")
            context = {
                "title": instance.First_Name + ' ' + instance.Last_Name,
                "instance": instance,
                "form": form,
            }
            return render(request, "mentee_form.html",context)

    else:
        context = {
            "title": "Please Log In"
        }
        return render(request, "base.html",context)


@login_required
def mentee_create(request):
    if request.user.is_authenticated():
        user = request.user
        res_user =  request.session.get('User', default=None)
        res_chapter =  request.session.get('Chapter', default=None)
        res_region =  request.session.get('Region', default=None)
        res_perm =  request.session.get('Perm', default=None)
        mentor = UserProfile.objects.filter(User=user)
        form = MenteeForm(request.POST or None)
        context = {
            "form": form,
        }
        if str(res_perm) == "Volunteer":
            messages.success(request, "You aren't authorized to view this record. If you feel this is in error please contact your Regional staff.")
            return render(request, "base.html")
        if str(res_perm) == "Chapter Staff":
            form.fields['Mentor_Assigned'].queryset = UserProfile.objects.filter(Chapter=res_chapter)
            form.fields['Chapter'].queryset = Chapter.objects.filter(Chapter_Name=res_chapter)
            form.fields['Region'].queryset = Region.objects.filter(Region_Name=res_region)

        if str(res_perm) == "Regional Staff":
            form.fields['Mentor_Assigned'].queryset = UserProfile.objects.filter(Region=res_region)
            form.fields['Chapter'].queryset = Chapter.objects.filter(Chapter_Regoin=res_region)
            form.fields['Region'].queryset = Region.objects.filter(Region_Name=res_region)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.Created_By = mentor
            instance.Updated_By = mentor
            instance.save()
            messages.success(request, "Successfully Created")
            return HttpResponseRedirect(instance.get_absolute_url())
        else:
            messages.error(request or None, "Not Successfully Created")
        return render(request, "mentee_form.html", context)
    else:
        context = {
            "title": "Please Log In"
        }
        return render(request, "base.html",context)


def log_activity_count(self, obj):
    obj.post_set.count()

# def mentee_delete(request):
    # return HttpResponse("<H1>delete</H1>")
