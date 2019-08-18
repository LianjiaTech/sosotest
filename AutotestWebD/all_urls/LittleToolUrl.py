from django.conf.urls import url
from apps.littletool.views import tool

urlpatterns = [
    #add page
    url(r'^littletool/jsoncn$', tool.jsoncn, name="LITTLETOOL_jsoncn"),

]