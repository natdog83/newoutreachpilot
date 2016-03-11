"""pilot URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

#from django.conf.urls.defaults import patterns, include, url
from django.conf.urls import include, url, patterns
from django.contrib.auth import views as auth_views
from django.contrib import admin
from django.contrib.auth import views
from mentee.views import mentee_home, mentee_list, mentee_detail, mentee_create, mentee_update
from login.views import login_user, logout_user, register_user, Mentor_List, passwordreset, password_change_done, Mentor_Table, mentor_detail
from log.views import logtable, Log_Create_Form, log_details

urlpatterns = [
    #url(r'^user/(?P<user_id>\d+)/user_edit/password/$', auth_views.password_change),
    #url('^', include('django.contrib.auth.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^password_change/$', passwordreset, name='passwordreset'),
    url(r'^password_change/done/$', password_change_done, name='password_change_done'),
    url(r'^register/', register_user, name='register'),
    url(r'^login/', login_user, name='login'),
    url(r'^logout/', logout_user, name='logout'),
    url(r'^ov/$', Mentor_List, name='outreachvolunteer'),
    url(r'^ov/table$', Mentor_Table, name='outreachvolunteertable'),
    url(r'^ov/(?P<id>\d+)/$', mentor_detail, name="mentor_detail"),
    url(r'^mentee/$', mentee_list, name='mentees'),
    url(r'^mentee/(?P<id>\d+)/$', mentee_detail, name="mentee_detail"),
    url(r'^activities/(?P<id>\d+)/$', log_details, name="logdetails"),
    url(r'^mentee/create/$', mentee_create, name='mentee_create'),
    url(r'^mentee/(?P<id>\d+)/edit/$', mentee_update, name="mentee_update"),
    url(r'^activities/$', logtable, name="activities"),
    url(r'^activities/new$', Log_Create_Form, name="newactivity"),   

    url(r'^$', mentee_home, name='home'),
]
