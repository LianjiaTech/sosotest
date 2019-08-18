from apps.common.func.CommonFunc import *
from apps.common.func.LanguageFunc import *
from django.shortcuts import render, HttpResponse
from apps.user_login.services.user_loginService import UserLoginService
from urllib import parse
from apps.user_center.services.user_http_confService import user_http_confService
from apps.common.config import commonWebConfig
import json
import hashlib
def user_token(request):
    langDict = getLangTextDict(request)
    context = {}

    context["user_token"] = "current-page"
    context["userName"] = request.session.get("userName")
    if not isRelease:
        context["env"] = "test"
    # 文本
    text = {}
    text["pageTitle"] = langDict["web"]["httpUserCenterUserHttpConfPageTitle"]
    text["subPageTitle"] = langDict["web"]["httpUserCenterUserHttpConfSubPageTitle"]
    context["text"] = text
    token = dbModelToDict(UserLoginService.getUserByLoginname(request.session.get("loginName"))[0])["token"]
    context["token"] = token if token else "NO TOKEN, GENERATE FIRST!"
    return render(request, "InterfaceTest/user_center/user_token.html", context)

def updateUserToken(request):
    loginName = request.session.get("loginName")
    token = "%s%s" % (loginName,datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    UserLoginService.updateMd5(loginName,hashlib.md5(token.encode(encoding='gb2312')).hexdigest())
    userToken = dbModelToDict(UserLoginService.getUserByLoginname(request.session.get("loginName"))[0])["token"]
    return HttpResponse(ApiReturn(body=userToken).toJson())


def jenkinsPlugin(request):
    langDict = getLangTextDict(request)
    context = {}
    context["user_token"] = "current-page"
    context["userName"] = request.session.get("userName")
    if not isRelease:
        context["env"] = "test"
    # 文本
    return render(request, "InterfaceTest/user_center/jenkins_plugin.html", context)
