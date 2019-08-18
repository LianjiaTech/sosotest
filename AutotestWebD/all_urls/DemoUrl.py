from django.conf.urls import url
from django.contrib import admin
from apps.demo.views import testViews

urlpatterns = [
    url(r'^testcdc', testViews.testcdc),
]