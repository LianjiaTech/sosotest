"""AutotestWebD URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
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
from all_urls import DefaultUrl,InvokeUrl,WebUrl,DemoUrl,WebPortalUrl,adminUrl,UiUrl,\
    DubboUrl,UiNewUrl,MockUrl,DataCollectorUrl,toolsUrl,DataKeywordUrl,StatisticTaskUrl,DubboHelpUrl,LittleToolUrl

urlpatterns = []
urlpatterns.extend(DefaultUrl.urlpatterns)
urlpatterns.extend(InvokeUrl.urlpatterns)
urlpatterns.extend(WebUrl.urlpatterns)
urlpatterns.extend(DemoUrl.urlpatterns)
urlpatterns.extend(WebPortalUrl.urlpatterns)
urlpatterns.extend(adminUrl.urlpatterns)
urlpatterns.extend(UiUrl.urlpatterns)
urlpatterns.extend(DubboUrl.urlpatterns)
urlpatterns.extend(UiNewUrl.urlpatterns)
urlpatterns.extend(MockUrl.urlpatterns)
urlpatterns.extend(DataCollectorUrl.urlpatterns)
urlpatterns.extend(toolsUrl.urlpatterns)
urlpatterns.extend(DataKeywordUrl.urlpatterns)
urlpatterns.extend(StatisticTaskUrl.urlpatterns)
urlpatterns.extend(DubboHelpUrl.urlpatterns)
urlpatterns.extend(LittleToolUrl.urlpatterns)


