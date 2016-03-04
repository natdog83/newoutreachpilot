from django.conf.urls import url
from django.contrib import admin
from .views import (
    mentee_list,
    mentee_create,
    mentee_detail,
    mentee_update,
    mentee_delete,
    mentee_home,
)

urlpatterns = [
    url(r'^', 'login.views.login_user' name='home'),
#    url(r'^mentees/$', mentee_list, name="mentee_list"),
#    url(r'^mentee/create/$', mentee_create),
#    url(r'^mentee/(?P<id>\d+)/edit/$', mentee_update, name="mentee_update"),
#    url(r'^mentee/delete/$', mentee_delete),