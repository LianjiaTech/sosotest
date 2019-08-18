from django.conf.urls import url
from django.contrib import admin
from apps.dubbo_help.views import dubboHelp

urlpatterns = [
    url(r'^dubbosug', dubboHelp.dubbo_sug),
]