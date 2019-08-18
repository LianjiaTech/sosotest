from django.conf.urls import url
from apps.invoke.views import InvokeViews

urlpatterns = [
    #invoke
    url(r'^invoke$', InvokeViews.index),
]