from apps.common.func.CommonFunc import *
from apps.common.func.LanguageFunc import *
from django.shortcuts import render, HttpResponse
from apps.user_login.services.user_loginService import UserLoginService
from urllib import parse
from apps.user_center.services.user_http_confService import user_http_confService
from apps.common.config import commonWebConfig
import json
import hashlib
def user_CI(request):
    langDict = getLangTextDict(request)
    context = {}

    context["user_CI"] = "current-page"
    context["userName"] = request.session.get("userName")
    if not isRelease:
        context["env"] = "test"
    # 文本
    text = {}
    context["text"] = text
    context["host"] = request.get_host()
    context["token"] = dbModelToDict(UserLoginService.getUserByLoginname(request.session.get("loginName"))[0])["token"]
    return render(request, "InterfaceTest/user_center/user_CI.html", context)
