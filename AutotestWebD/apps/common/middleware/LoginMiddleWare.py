from django.conf import settings
from django.utils.deprecation import MiddlewareMixin
from apps.common.func.AAA import *
from apps.user_login.views.user_login import index
from apps.myadmin.views.login import doLogin
from apps.common.func.WebFunc import addUserLog

class LoginMiddleWare(MiddlewareMixin):
    def process_request(self, request):
        requestUrl = request.path
        addUserLog(request, "MiddleWare", "PASS")
        needFilt = True
        if requestUrl==settings.LOGIN_URL:
            needFilt = False
        else:
            for noAuthUrl in settings.NO_AUTH_URLS:
                if requestUrl.startswith(noAuthUrl):
                    needFilt = False
                    break
        if needFilt:
            adminFilt = False
            for adminAuthUrl in settings.MYADMIN_URLS:
                if requestUrl.startswith(adminAuthUrl):
                    adminFilt = True
                    break
            if adminFilt:
                adminAuthInfo = adminAAA(request)
                if adminAuthInfo[0] == False:
                    return doLogin(request)
            else:
                authInfo = AAAUser(request)
                redirectUrlList = [
                    "/interfaceTest/HTTP_InterfaceCheck",
                    "/dubbo/interfaceList",
                    "/mockserver/HTTP_InterfaceCheck",
                    "/interfaceTest/HTTP_operationInterface",
                    "/interfaceTest/HTTP_InterfaceAddPage",
                    "/interfaceTest/importPostmanPage",
                    "/dubbo/importLogPage",
                    "/interfaceTest/HTTP_TestCaseCheck",
                    "/interfaceTest/HTTP_TestCaseStepCheck",
                    "/interfaceTest/HTTP_TestCaseAddPage",
                    "/interfaceTest/HTTP_TaskCheck",
                    "/interfaceTest/HTTP_TaskSuiteCheck",
                    "/dubbo/operationInterface",
                    "/dubbo/interfaceAddPage",
                    "/statistictask/execlistPage",
                    "/statistictask/listPage",
                    "/statistictask/operationCheck",
                    "/interfaceTest/HTTP_EnvUriConf",
                    "/interfaceTest/HTTP_UserHttpConf",
                    "/interfaceTest/HTTP_UriConf",
                    "/interfaceTest/HTTP_UserServiceConf",
                    "/interfaceTest/HTTP_GlobalVarsConf",
                    "/interfaceTest/HTTP_GlobalTextConf",
                    "/datakeyword/listPage",
                    "/datakeyword/operationCheck",
                    "/interfaceTest/HTTP_operationTestCase",
                    "/dubbo/operationTestCase",
                ]
                if request.META["PATH_INFO"] in  redirectUrlList:
                    request.session["nextUrl"] = request.META["PATH_INFO"] + ("" if request.META["QUERY_STRING"] == "" else "?"+request.META["QUERY_STRING"])
                if authInfo[0] == False:
                    return index(request)