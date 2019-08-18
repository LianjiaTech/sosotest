from django.shortcuts import render
from django.shortcuts import HttpResponse,redirect
from apps.myadmin.service.AdminLoginService import AdminLoginService
# Create your views here.
from all_models.models import TbUser, TbAdminUser
from apps.common.func.WebFunc import *
from apps.common.func.AAA import *
from apps.myadmin.service.AdminUserService import AdminUserService


def loginPage(request):

    if "adminAudit" in request.session and request.session["adminAudit"] == 1:
        # return HttpResponseRedirect('/myadmin/changeLog/check')
        return render(request, "myadmin/home.html", {})

    return render(request,"myadmin/login.html",{})

def home(request):

    return render(request,"myadmin/home.html",{})

def doLogin(request):
    loginName = request.POST.get("loginName","")
    passWord = request.POST.get("passWord","")
    if loginName == None or passWord == None:
        return HttpResponse(ApiReturn(ApiReturn.CODE_WARNING,body="登录状态不正确").toJson())
    pwdMd5 = hashlib.md5()
    pwdMd5.update(passWord.encode("utf-8"))
    userData = AdminLoginService.getUserLoginType(loginName, pwdMd5.hexdigest())
    if userData:
        addAdminSession(request, dbModelToDict(userData[0]))
        return HttpResponse(ApiReturn().toJson())
    else:
        return HttpResponse(ApiReturn(ApiReturn.CODE_WARNING,body="用户名或密码错误",message="<script>window.location.href = '/myadmin/login'</script>").toJson())

def changePassword(request):
    userData = json.loads(request.POST.get("userData"))

    password = userData["password"]
    password1 = userData["password1"]

    if password != password1:
        return HttpResponse(ApiReturn(ApiReturn.CODE_ERROR, body="两次输入密码不一致，请重新输入").toJson())
    loginName = request.session.get("adminLoginName")

    pwdMd5 = hashlib.md5()
    pwdMd5.update(password.encode("utf-8"))
    adminUserList = dbModelListToListDict(TbAdminUser.objects.filter(loginName=loginName, state=1))
    adminUserList[0]["passWord"] = pwdMd5.hexdigest()
    AdminUserService.updateAdminUser(adminUserList[0])
    return HttpResponse(ApiReturn().toJson())


def logout(request):
    delAdminSession(request)
    return redirect("/myadmin/login")