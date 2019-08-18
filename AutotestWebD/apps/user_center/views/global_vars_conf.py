from apps.common.func.CommonFunc import *
from apps.common.func.LanguageFunc import *
from django.shortcuts import render, HttpResponse
from apps.config.services.serviceConfService import ServiceConfService
from apps.config.services.http_confService import HttpConfService
from urllib import parse
from apps.common.config import commonWebConfig
from apps.user_center.services.global_varsService import global_varsService
from apps.common.func.WebFunc import getServiceConf
import json
from apps.version_manage.services.common_service import VersionService
from django.views.decorators.csrf import csrf_exempt
from apps.common.decorator.permission_normal_funcitons import *

def globalVarsCheck(request):
    langDict = getLangTextDict(request)
    context = {}

    context["httpUserCenterGlobalVarsPage"] = "current-page"
    context["userName"] = request.session.get("userName")
    if not isRelease:
        context["env"] = "test"

    context.update(getServiceConf(request))
    # 文本
    text = {}
    text["pageTitle"] = langDict["web"]["httpUserCenterGlobalVarsPageTitle"]
    text["subPageTitle"] = langDict["web"]["httpUserCenterGlobalVarsSubPageTitle"]
    context["text"] = text
    context["title"] = "全局变量"

    context["page"] = 1
    return render(request, "InterfaceTest/user_center/global_vars_conf.html", context)


def queryVars(request):

    page = request.POST.get("page")
    if isInt(page):
        page = int(page)
    else:
        return HttpResponse("<script>alert('请验证页数参数');</script>")

    checkArr = json.loads(parse.unquote(request.POST.get("queryArr")))

    orderBy = request.POST.get("orderBy")
    if isSqlInjectable(orderBy):
        return HttpResponse("<script>alert('查询条件非法');</script>")

    #根据版本判断应该从哪个表里取数据 王吉亮添加于20180224
    if VersionService.isCurrentVersion(request):
        tbName = "tb_global_vars"
        versionCondition = ""
    else:
        tbName = "tb_version_global_vars"
        versionCondition = "and versionName='%s'" % request.session.get("version")

    execSql = "SELECT g.*,u.userName,umod.userName modByName FROM %s g LEFT JOIN tb_user u ON g.addBy = u.loginName  LEFT JOIN tb_user umod ON g.modBy = umod.loginName WHERE g.state=1 %s " % (tbName,versionCondition)
    checkList = []
    for key in checkArr:
        if checkArr[key] == "":
            continue
        elif key == "addBy":
            checkList.append("%%%s%%" % checkArr[key])
            checkList.append("%%%s%%" % checkArr[key])
            execSql += """ and (g.addBy LIKE %s or u.userName LIKE %s) """

            continue
        checkList.append("%%%s%%" % checkArr[key])
        execSql += """ and g.%s """ % key
        execSql += """ LIKE %s"""
    execSql += """ ORDER BY %s""" % orderBy
    context = pagination(sqlStr=execSql, attrList=checkList, page=page, pageNum=commonWebConfig.testCasePageNum,request=request)

    context.update(getServiceConf(request))
    response = render(request, "InterfaceTest/user_center/SubPages/global_vars_conf_sub_page.html", context)
    return response

@single_data_permission(TbGlobalVars,TbVersionGlobalVars)
def varsConfDel(request):
    id = request.GET.get("id")
    if VersionService.isCurrentVersion(request):
        getVar = global_varsService.getVar(id)
        if getVar.addBy.loginName != request.session.get("loginName"):
            changeLog = TbUserChangeLog()
            changeLog.version = request.session.get("version")
            changeLog.loginName = request.session.get("loginName")
            changeLog.otherLoginName = getVar.addBy.loginName
            changeLog.type = 0
            changeLog.beforeChangeData = dictToJson(dbModelToDict(getVar))
            changeLog.dataId = getVar.varKey
            changeLog.changeDataId = getVar.varKey
            changeLog.save()

        try:
            global_varsService.delVar(id)
            return HttpResponse(ApiReturn(ApiReturn.CODE_OK).toJson())
        except Exception as e:
            return HttpResponse(ApiReturn(ApiReturn.CODE_GLOBAL_EXCEPITON,e).toJson())
    else:
        getVar = global_varsService.getVersionVar(id)
        if getVar.addBy.loginName != request.session.get("loginName"):
            changeLog = TbUserChangeLog()
            changeLog.version = request.session.get("version")
            changeLog.loginName = request.session.get("loginName")
            changeLog.otherLoginName = getVar.addBy.loginName
            changeLog.type = 0
            changeLog.beforeChangeData = dictToJson(dbModelToDict(getVar))
            changeLog.dataId = getVar.varKey
            changeLog.changeDataId = getVar.varKey
            changeLog.save()
        try:
            global_varsService.delVersionVar(id)
            return HttpResponse(ApiReturn(ApiReturn.CODE_OK).toJson())
        except Exception as e:
            return HttpResponse(ApiReturn(ApiReturn.CODE_GLOBAL_EXCEPITON, e).toJson())

def getVarsConf(request):
    id = request.GET.get("id")

    if VersionService.isCurrentVersion(request):
        varData = dbModelToDict(global_varsService.getVar(id))
    else:
        varData = dbModelToDict(global_varsService.getVersionVar(id))

    serviceConf = ServiceConfService.queryServiceConfSort(request)
    varData["serviceConf"] = {}
    varData["serviceConf"]["common"] = substr(varData["varValue"], "[CONF=common]", "[ENDCONF]")
    for i in range(0, len(serviceConf)):
        if serviceConf[i]["serviceConfKey"] not in varData["varValue"]:
            varData["serviceConf"]["%s" % serviceConf[i]["serviceConfKey"]] = ""
            continue
        varData["serviceConf"]["%s" % serviceConf[i]["serviceConfKey"]] = substr(varData["varValue"],"[CONF=%s]" % serviceConf[i]["serviceConfKey"],"[ENDCONF]")
    return HttpResponse(ApiReturn(body=varData).toJson())

@single_data_permission(TbGlobalVars,TbVersionGlobalVars)
def varsConfAdd(request):
    varData = json.loads(parse.unquote(request.POST.get("data")))
    varData["addBy_id"] = request.session.get("loginName")
    try:
        if VersionService.isCurrentVersion(request):
            global_varsService.addVar(varData)
        else:
            global_varsService.addVersionVar(varData,VersionService.getVersionName(request))
    except Exception as e:
        return HttpResponse(ApiReturn(ApiReturn.CODE_GLOBAL_EXCEPITON,"key重复").toJson())
    return HttpResponse(ApiReturn().toJson())

@single_data_permission(TbGlobalVars,TbVersionGlobalVars)
def varsConfEdit(request):
    varData = json.loads(parse.unquote(request.POST.get("data")))
    varData["modBy"] = request.session.get("loginName")
    if VersionService.isCurrentVersion(request):
        getVar = global_varsService.getVar(varData["id"])
        if getVar.addBy.loginName != request.session.get("loginName"):
            changeLog = TbUserChangeLog()
            changeLog.version = request.session.get("version")
            changeLog.loginName = request.session.get("loginName")
            changeLog.otherLoginName = getVar.addBy.loginName
            changeLog.type = 1
            changeLog.beforeChangeData = dictToJson(dbModelToDict(getVar))
            changeLog.afterChangeData = dictToJson(varData)
            changeLog.dataId = getVar.varKey
            changeLog.changeDataId = getVar.varKey
            changeLog.save()
        global_varsService.editVar(varData)
        return HttpResponse(ApiReturn().toJson())
    else:
        getVar = global_varsService.getVersionVar(varData["id"])
        if getVar.addBy.loginName != request.session.get("loginName"):
            changeLog = TbUserChangeLog()
            changeLog.version = request.session.get("version")
            changeLog.loginName = request.session.get("loginName")
            changeLog.otherLoginName = getVar.addBy.loginName
            changeLog.type = 1
            changeLog.beforeChangeData = dictToJson(dbModelToDict(getVar))
            changeLog.afterChangeData = dictToJson(varData)
            changeLog.dataId = getVar.varKey
            changeLog.changeDataId = getVar.varKey
            changeLog.save()
        global_varsService.editVersionVar(varData,VersionService.getVersionName(request))
        return HttpResponse(ApiReturn().toJson())

@csrf_exempt
def getGlobalVarForVarKey(request):
    varKey = request.GET.get("varKey",None)
    token = request.GET.get("token",None)

    if varKey == None:
        return HttpResponse(ApiReturn(ApiReturn.CODE_ERROR,message="参数varKey 不能为空").toJson())

    if token == None:
        return HttpResponse(ApiReturn(ApiReturn.CODE_ERROR,message="参数token 不能为空").toJson())

    getUser = TbUser.objects.filter(token=token,state=1)
    if len(getUser) == 0:
        return HttpResponse(ApiReturn(ApiReturn.CODE_ERROR, message="参数token 查询用户错误").toJson())

    getVar = TbGlobalVars.objects.filter(varKey=varKey,state=1)
    if len(getVar) == 0:
        return HttpResponse(ApiReturn(ApiReturn.CODE_ERROR, message="参数varKey 查询全局变量错误").toJson())
    serviceConfList = ServiceConfService.getServiceConf()
    varData = getVar.last().varValue
    retVar = {}
    if "[CONF=common]" in varData:
        retVar["common"] = substr(varData,"[CONF=common]","[ENDCONF]")
    for serviceIndex in serviceConfList:
        if "[CONF=%s]" % serviceIndex["serviceConfKey"] not in varData:
            continue
        retVar[serviceIndex["serviceConfKey"]] = substr(varData,"[CONF=%s]" % serviceIndex["serviceConfKey"],"[ENDCONF]")

    return HttpResponse(ApiReturn(ApiReturn.CODE_OK, body=retVar).toJson())

@csrf_exempt
def setGlobalVarForVarKey(request):
    varKey = request.POST.get("varKey", None)
    token = request.POST.get("token", None)
    varValue = request.POST.get("varValue", None)

    if varKey == None:
        return HttpResponse(ApiReturn(ApiReturn.CODE_ERROR, message="参数varKey 不能为空").toJson())

    if token == None:
        return HttpResponse(ApiReturn(ApiReturn.CODE_ERROR, message="参数token 不能为空").toJson())

    getUser = TbUser.objects.filter(token=token, state=1)
    if len(getUser) == 0:
        return HttpResponse(ApiReturn(ApiReturn.CODE_ERROR, message="参数token 查询用户错误").toJson())

    getVar = TbGlobalVars.objects.filter(varKey=varKey, state=1)
    if len(getVar) == 0:
        return HttpResponse(ApiReturn(ApiReturn.CODE_ERROR, message="参数varKey 查询全局变量错误").toJson())
    if type(varValue) == type(""):
        if not isJson(varValue):
            return HttpResponse(ApiReturn(ApiReturn.CODE_ERROR, message="参数varValue不是JSON格式").toJson())
        varDict = json.loads(varValue)

    else:
        try:
            varDict = eval(varValue)
        except:
            return HttpResponse(ApiReturn(ApiReturn.CODE_ERROR, message="参数varValue不是JSON格式").toJson())
    serviceConfList = ServiceConfService.getServiceConf()
    serviceList = []
    for serviceIndex in serviceConfList:
        serviceList.append(serviceIndex["serviceConfKey"])

    varText = ""
    for index in varDict:
        if index !="common" and index not in serviceList:
            print(index)
            return HttpResponse(ApiReturn(ApiReturn.CODE_ERROR,"varValue中存在Key不为HTTPConfKey").toJson())
        varText += "[CONF=%s]%s[ENDCONF]" % (index,varDict[index])
    varData = getVar.last()
    varData.varValue = varText
    varData.modBy = getUser.last().loginName
    varData.save()


    return HttpResponse(ApiReturn(ApiReturn.CODE_OK).toJson())