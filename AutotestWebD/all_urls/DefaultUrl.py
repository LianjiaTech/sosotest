from django.conf.urls import url
from django.contrib import admin
from apps.demo.views import LoginViews


urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    #user
    url(r'^user/resp$',  LoginViews.response),
    url(r'^testsql$',  LoginViews.testsql),
    url(r'^testsql2$', LoginViews.testsql2),
]