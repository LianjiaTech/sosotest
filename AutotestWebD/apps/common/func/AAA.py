from apps.user_login.services import user_loginService
from django.shortcuts import HttpResponse,HttpResponseRedirect
import datetime
from all_models.models.A0011_version_manage import TbVersion
from apps.version_manage.services.common_service import VersionService
from AutotestWebD.settings import *

def AAAUser(request):
    # 判断用户状态
    audit =  request.session.get("audit")
    if audit == 0:
        return [False,"用户状态为未审核，请联系管理员"]
    elif audit == 1:
        return [False,"用户状态为审核中，请联系管理员"]
    elif audit == 2:
        return [True]
    elif audit == 3:
        return [False, "用户状态为未通过，请联系管理员"]
    else:
        return [False, "用户状态未知，请登录"]

def addCookie(response,userData):
    now = (datetime.datetime.now() + datetime.timedelta(days=7 * 4 * 12))
    response.set_cookie("audit", userData[0].audit, expires=now)
    response.set_cookie("loginName", userData[0].loginName, expires=now)
    response.set_cookie("pwd", userData[0].pwd, expires=now)

def delCookie(response):
    response.delete_cookie("loginName")
    response.delete_cookie("pwd")
    response.delete_cookie("audit")

    response.delete_cookie("jiraUserName")
    response.delete_cookie("jiraPassword")
    response.delete_cookie("gerritUserName")
    response.delete_cookie("gerritPassword")
    response.delete_cookie("releasemgrUserName")
    response.delete_cookie("releasemgrPassword")
    response.delete_cookie("filterId")
    response.delete_cookie("OPS_Type")

def addSession(request,data):
    #addSession
    #设置session关闭浏览器才失效
    request.session.set_expiry(0)
    request.session["loginName"] = data[0].loginName
    request.session["userName"] = data[0].userName
    request.session["id"] = data[0].id
    request.session["audit"] = data[0].audit
    VersionService.setToCurrentVersion(request)
    VersionService.setLastVersionSession(request)

def delSession(request):
    if "loginName" in request.session:
        del request.session["loginName"]
    if "userName" in request.session:
        del request.session["userName"]
    if "id" in request.session:
        del request.session["id"]
    if "audit" in request.session:
        del request.session["audit"]
    if "version" in request.session:
        del request.session["version"]
    if "LastVersion" in request.session:
        del request.session["LastVersion"]
    if "CurrentVersion" in request.session:
        del request.session["CurrentVersion"]
    if "groupLevel1" in request.session:
        del request.session['groupLevel1']
    if "groupLevel2" in request.session:
        del request.session['groupLevel2']
    if "env" in request.session:
        del request.session['env']

def adminAAA(request):
    audit = request.session.get("adminAudit",0)
    if audit == 0:
        return [False,"用户未登录"]
    else:
        return [True]

def addAdminSession(request,userData):
    request.session["adminLoginName"] = userData["loginName"]
    request.session["adminAudit"] = 1
    request.session["adminUserName"] = userData["userName"]
    request.session["superManager"] = userData["superManager"]
    request.session['isReleaseEnv'] = isRelease

def delAdminSession(request):
    if "adminLoginName" in request.session:
        del request.session["adminLoginName"]
    if "adminAudit" in request.session:
        del request.session["adminAudit"]
    if "adminUserName" in request.session:
        del request.session["adminUserName"]
    if "superManager" in request.session:
        del request.session["superManager"]
    if "isReleaseEnv" in request.session:
        del request.session['isReleaseEnv']