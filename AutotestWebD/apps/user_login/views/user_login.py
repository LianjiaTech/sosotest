from django.shortcuts import HttpResponse,redirect,HttpResponseRedirect,render
from apps.user_login.services.user_loginService import UserLoginService
from apps.common.func.AAA import delCookie,addCookie,addSession,delSession
from apps.common.func.LanguageFunc import *
from apps.common.helper.ApiReturn import ApiReturn
import hashlib
from AutotestWebD.settings import *
from django.contrib import auth
import logging
logger = logging.getLogger("django")

def index(request):
    request.session['site_name'] = SITE_NAME
    cookie = request.COOKIES
    userName = ""
    if "audit" in cookie.keys():      #判断COOKIE
        userName = cookie.get("loginName")
    if "audit" in request.session:
        userName = request.session["loginName"]
    if userName:
        userData = UserLoginService.getUserLoginMsg(userName, cookie.get("pwd"))
        if userData:
            if userData[0].audit != 2:
                response = HttpResponse("'<script>alert('用户状态不对，请联系管理员');window.location='/'</script>'")
                delCookie(response)
                return response
            addSession(request, userData)  # 添加session
            if request.session.get("nextUrl"):
                response = HttpResponseRedirect(request.session.get("nextUrl"))
                del request.session["nextUrl"]
            else:
                response = HttpResponseRedirect('/interfaceTest/HTTP_InterfaceCheck')
            setLanguage(request, response,DEFAULT_LANGUAGE)
            return response
        else:
            response = HttpResponse("'<script>alert('用户名密码错误');window.location='/user/login'</script>'")
            delCookie(response)
            delSession(request)
            return response

    return render(request, "user_login/UserLogin.html")

def userLogin(request):
    userName = request.POST.get("username")
    pwd = request.POST.get("password")
    isLoginUserSelfUser = False
    if LDAP_ENABLED:
        #先执行LDAP登录
        logger.debug("%s 开始ldap登录" % userName)
        user = auth.authenticate(username=userName, password=pwd)
        logger.debug("#############TESTFORLDAP--NEW#######################")
        logger.debug(user)
        logger.debug(type(user))
        logger.debug("#############TESTFORLDAP--END#######################")

        if user is not None and user.is_active:
            userData = UserLoginService.getUserByLoginname(userName)
            if userData:
                newUser = userData[0]
                if userData[0].audit != 2:
                    response = HttpResponse("'<script>alert('用户状态不对，请联系管理员');window.location='/'</script>'")
                    delCookie(response)
                    return response
                else:
                    newUser.email = user.email
                    newUser.userName = user.first_name.split("(")[0]
                    pwdMd5 = hashlib.md5()
                    pwdMd5.update(pwd.encode("utf-8"))
                    newUser.pwd = pwdMd5.hexdigest()
                    newUser.save(force_update = True)
                    addSession(request, userData)  # 添加session
                    logger.debug("%s LDAP登录成功且存在用户！" % newUser.userName)
                    if request.session.get("nextUrl"):
                        response = HttpResponseRedirect(request.session.get("nextUrl"))
                        del request.session["nextUrl"]
                    else:
                        response = HttpResponseRedirect('/interfaceTest/HTTP_InterfaceCheck')

                    if request.POST.get("category"):
                        addCookie(response, userData)
                    return response
            else:
                newUser = TbUser()
                newUser.loginName = userName
                newUser.email = user.email
                newUser.userName = user.first_name.split("(")[0]
                pwdMd5 = hashlib.md5()
                pwdMd5.update(pwd.encode("utf-8"))
                newUser.pwd = pwdMd5.hexdigest()
                newUser.type = 2
                newUser.audit = 2
                newUser.save(force_insert=True)
                logger.debug("%s LDAP登录成功但不存在用户！" % newUser.userName)
                response = HttpResponse("'<script>alert('用户名密码错误');window.location='/'</script>'")
                return response
        else:
            logger.debug("LDAP falure!")
            isLoginUserSelfUser = True
    else:
        isLoginUserSelfUser = True

    if isLoginUserSelfUser:
        if(userName == None or pwd == None):
            response = HttpResponse("'<script>alert('用户名密码错误');window.location='/'</script>'")
            return response
        pwdMd5 = hashlib.md5()
        pwdMd5.update(pwd.encode("utf-8"))
        userData = UserLoginService.getUserLoginMsg(userName,pwdMd5.hexdigest())
        if userData:
            if userData[0].audit != 2:
                response = HttpResponse("'<script>alert('用户状态不对，请联系管理员');window.location='/'</script>'")
                delCookie(response)
                return response
            else:
                addSession(request, userData)  # 添加session
                if request.session.get("nextUrl"):
                    response = HttpResponseRedirect(request.session.get("nextUrl"))
                    del request.session["nextUrl"]
                else:
                    response = HttpResponseRedirect('/interfaceTest/HTTP_InterfaceCheck')

                if request.POST.get("category"):
                    addCookie(response, userData)
                logger.debug("%s 非ldap登录成功！" % userName)


                return response
        else:
            response = HttpResponse("'<script>alert('用户名密码错误');window.location='/'</script>'")
            return response



def redirectUrl(request):
    if request.session.get("loginName"):
        return redirect("/user/login")
    else:
        context = {
            "SITE_NAME":SITE_NAME
        }
        return render(request,"index.html",context)


def userLoginTestGetCookie(request):
    cookie = request.COOKIES
    # userName = request.POST.get("username")
    # passWord = request.POST.get("password")

    # return HttpResponse(request.COOKIES.get("pwd")+"    "+str(request.session.get("loginName")))
    # now =  (datetime.datetime.now() + datetime.timedelta(days = 7*4*12))
    # now.day += (now.day*7*64)
    # now.day = now.day*7*64
    return HttpResponse(cookie.get("asdadasdsada") == None)

def logout(request):
    delSession(request)
    response = HttpResponseRedirect("/")
    delCookie(response)
    return response

def updatePwd(request):
    pwd = request.GET.get("pwd")

    m = hashlib.md5(pwd.encode(encoding='gb2312'))
    modPwd = m.hexdigest()
    try:
        UserLoginService.updatePwd(request.session.get("loginName"),modPwd)
        return HttpResponse(ApiReturn(ApiReturn.CODE_OK).toJson())
    except Exception as e:
        return HttpResponse(ApiReturn(ApiReturn.CODE_USER_EXCEPITON,"修改失败，请联系管理员%s" % e).toJson())




if __name__ == "__main__":
    md5Pwd = hashlib.md5()
    md5Pwd.update(b"123456")
    md5Pwd.hexdigest()
    print( md5Pwd.hexdigest())
