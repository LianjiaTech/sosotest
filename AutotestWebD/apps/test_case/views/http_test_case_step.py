from django.shortcuts import render,HttpResponse
from urllib import parse
from apps.test_case.services.HTTP_test_caseService import HTTP_test_caseService
from apps.test_case.services.HTTP_test_case_stepService import HTTP_test_case_stepService
from apps.interface.services.HTTP_interfaceService import HTTP_interfaceService
from apps.test_case.services.HTTP_test_case_debugService import HTTP_test_case_debugService
from apps.test_case.services.HTTP_test_case_step_debugService import HTTP_test_case_step_debugService
from apps.common.config import commonWebConfig
from apps.common.func.CommonFunc import *
from apps.common.func.LanguageFunc import *
from apps.config.services.businessLineService import BusinessService
from apps.config.services.modulesService import ModulesService
from apps.config.services.uriService import UriService
from apps.config.services.serviceConfService import ServiceConfService
from apps.config.services.http_confService import HttpConfService
from apps.config.views.http_conf import getDebugBtn
from apps.common.func.WebFunc import *
from AutotestWebD.settings import isRelease
import json,time
from apps.version_manage.services.common_service import VersionService


def http_testCaseStepCheck(request):
    context = {}

    context["testCaseStepCheck"] = "current-page"
    context["userName"] = request.session.get("userName")
    context["checkBusinessLine"] = dbModelListToListDict(BusinessService.getAllBusinessLine())
    context["checkModules"] = dbModelListToListDict(ModulesService.getAllModules())
    if not isRelease:
        context["env"] = "test"
    #文本
    text = {}
    text["pageTitle"] = "HTTP用例步骤查看"
    context["text"] = text
    context["uri"] = UriService.getUri(request,"HTTP")
    context["page"] = 1
    return render(request,"InterfaceTest/HTTPTestCase/HTTP_testCaseStep_check.html",context)

def http_testCaseStepListCheck(request):
    page = request.POST.get("page")
    if isInt(page):
        page = int(page)
    else:
        return HttpResponse("<script>alert('请验证页数参数');</script>")

    checkArr = json.loads(parse.unquote(request.POST.get("checkVal")))

    orderBy = request.POST.get("orderBy")
    if isSqlInjectable(orderBy):
        return HttpResponse("<script>alert('查询条件非法');</script>")

    #根据版本判断应该从哪个表里取数据 王吉亮添加于20180224
    if VersionService.isCurrentVersion(request):
        tbName = "tb_http_testcase_step"
        versionCondition = ""
    else:
        tbName = "tb_version_http_testcase_step"
        versionCondition = "and versionName='%s'" % request.session.get("version")


    execSql = "SELECT t.*,u.userName,m.moduleName,b.bussinessLineName,mu.userName modByName,tc.id tid from %s t LEFT JOIN tb_user mu ON t.modBy = mu.loginName LEFT JOIN tb_modules m on t.moduleId = m.id LEFT JOIN tb_business_line b on t.businessLineId = b.id LEFT JOIN tb_user u ON t.addBy = u.loginName LEFT JOIN tb_http_testcase tc ON t.caseId = tc.caseId  WHERE 1=1 and t.state=1 %s" % (tbName,versionCondition)
    checkList = []
    for key in checkArr:
        if checkArr[key] == "":
            continue
        elif key == "caseFounder" :
            checkList.append("%%%s%%" % checkArr[key])
            checkList.append("%%%s%%" % checkArr[key])
            execSql += """ and (t.addBy LIKE %s or u.userName LIKE %s) """
            continue
        elif key == "module":
            checkList.append("%%%s%%" % checkArr[key])
            execSql += """ and m.moduleName LIKE %s """
            continue
        elif key == "businessLine":
            checkList.append("%%%s%%" % checkArr[key])
            execSql += """ and b.bussinessLineName LIKE %s """
            continue
        elif key == "fromInterfaceId":
            checkList.append("%%%s%%" % checkArr[key])
            execSql += """ and t.fromInterfaceId LIKE %s and isSync = 1 """
            continue
        checkList.append("%%%s%%" % checkArr[key])
        execSql += """ and t.%s """ % key
        execSql += """ LIKE %s"""
    execSql += """ ORDER BY %s""" % orderBy

    context = pagination(sqlStr=execSql,attrList=checkList,page=page,pageNum=commonWebConfig.testCasePageNum,request=request)
    response = render(request, "InterfaceTest/HTTPTestCase/SubPages/HTTP_testCaseStep_list_check_page.html",context)
    return response
