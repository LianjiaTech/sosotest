from apps.common.func.CommonFunc import *
from apps.common.func.LanguageFunc import *
from django.shortcuts import render, HttpResponse
from all_models.models import *
from urllib import parse
from apps.user_center.services.user_http_confService import user_http_confService
from apps.common.config import commonWebConfig
from apps.config.services.serviceConfService import ServiceConfService
from apps.config.services.http_confService import HttpConfService
from apps.config.services.uriService import UriService
from apps.common.decorator.permission_normal_funcitons import *
import json

def userHttpConfCheck(request):
    langDict = getLangTextDict(request)
    context = {}

    context["httpUserCenterUserHttpConfPage"] = "current-page"
    context["userName"] = request.session.get("userName")
    if not isRelease:
        context["env"] = "test"
    # 文本
    text = {}
    text["pageTitle"] = langDict["web"]["httpUserCenterUserHttpConfPageTitle"]
    text["subPageTitle"] = langDict["web"]["httpUserCenterUserHttpConfSubPageTitle"]
    context["text"] = text
    serviceConf = ServiceConfService.getServiceConf()
    context["services"] = serviceConf
    # context["uriServices"] = UriService.getUri(request)
    # context["dubboServices"] = dbModelListToListDict(TbConfigUri.objects.filter(state=1,protocol="DUBBO").order_by("level"))
    context["envConfList"] = HttpConfService.getAllHttpConf(request)
    # context["uri"] = UriService.getUri(request, "ALL")
    context["page"] = 1
    context["title"] = "环境配置"

    return render(request, "InterfaceTest/user_center/user_http_conf.html", context)

def getHttpConfData(request):
    id = request.GET.get("id")
    httpConfData = dbModelToDict(HttpConfService.getHttpConfForId(id))
    httpConfList = httpConfData["httpConf"].split("\n")
    result = []
    loop = 0
    for httpConfIndex in range (1,len(httpConfList)):
        if httpConfList[httpConfIndex] == "" or "=" not in httpConfList[httpConfIndex]:
            continue

        indexData = httpConfList[httpConfIndex].split("=")
        result.append({})
        result[loop]["httpConfKey"] = indexData[0].strip()
        result[loop]["httpConfValue"] = indexData[1].strip()

        loop += 1
    return HttpResponse(ApiReturn(body=result).toJson())


def queryUserHttpConf(request):
    page = request.POST.get("page")
    if isInt(page):
        page = int(page)
    else:
        return HttpResponse("<script>alert('请验证页数参数');</script>")
    checkArr = json.loads(parse.unquote(request.POST.get("queryArr")))

    execSql = "SELECT c.*,us.userName,cs.alias serviceAlias FROM tb_config_http c LEFT JOIN (select * from tb_user_httpconf where loginName = '%s' ) u ON c.httpConfKey=u.httpConfKey INNER JOIN tb_user us ON c.addBy = us.loginName INNER JOIN tb_config_service cs ON c.serviceConfKey= cs.serviceConfKey WHERE 1=1 AND c.state=1" % request.session.get("loginName")
    checkList = []
    for key in checkArr:
        if checkArr[key] == "":
            if key == "typeConf":
                execSql += """ and ( """
                showMenuConfig = eval(confDict['COMMON']['showMenuConfig'])
                indexCount = 0
                for index in showMenuConfig:
                    if showMenuConfig[index] == 1:
                        if indexCount == 0:
                            if index == "HttpInterface" or index == "UI":
                                execSql += " apiRunState = 1 "
                            elif index == "DubboInterface":
                                execSql += " dubboRunState = 1 "
                        else:
                            if index == "HttpInterface" or index == "UI":
                                execSql += " OR apiRunState = 1 "
                            elif index == "DubboInterface":
                                execSql += " OR dubboRunState = 1 "
                        indexCount += 1
                execSql += """ ) """
            continue
        elif key == "typeConf":
            typeConfList = checkArr[key].split(",")
            for index in typeConfList:
                if index == "http":
                    execSql += """ and c.apiRunState = 1 """
                elif index == 'ui':
                    execSql += """ and c.uiRunState = 1 """
                elif index == 'dubbo':
                    execSql += """ and c.dubboRunState = 1 """
            continue
        elif key == "addBy":
            checkList.append("%%%s%%" % checkArr[key])
            checkList.append("%%%s%%" % checkArr[key])
            execSql += """ and (c.addBy LIKE %s or us.userName LIKE %s) """
            continue
        checkList.append("%%%s%%" % checkArr[key])
        execSql += """ and c.%s """ % key
        execSql += """ LIKE %s"""
    execSql += """ ORDER BY u.conflevel is null,u.conflevel asc, c.modTime desc"""
    context = pagination(execSql, checkList, page, commonWebConfig.userHttpConfPageNum,request=request)
    context["uriServices"] = UriService.getUri(request)
    context["dubboServices"] = dbModelListToListDict(TbConfigUri.objects.filter(state=1,protocol="DUBBO").order_by("level"))

    response = render(request, "InterfaceTest/user_center/SubPages/user_http_conf_sub_page.html", context)
    return response

@single_data_permission(TbUserHttpconf,TbUserHttpconf)
def userHttpConfDel(request):
    id = request.GET.get("id")
    getVar = user_http_confService.getUserHttpConf(id)
    if getVar.addBy.loginName != request.session.get("loginName"):
        return HttpResponse(ApiReturn(ApiReturn.CODE_GLOBAL_EXCEPITON,"只能删除自己的变量").toJson())
    try:
        user_http_confService.delUserHttpConf(id)
        return HttpResponse(ApiReturn(ApiReturn.CODE_OK).toJson())
    except Exception as e:
        return HttpResponse(ApiReturn(ApiReturn.CODE_GLOBAL_EXCEPITON,e).toJson())

@single_data_permission(TbUserHttpconf,TbUserHttpconf)
def httpConfAdd(request):
    showMenuConfig = eval(confDict['COMMON']['showMenuConfig'])
    varData = json.loads(parse.unquote(request.POST.get("data")))
    for index in showMenuConfig:
        if showMenuConfig[index] == 1:
            if index == "HttpInterface":
                varData["apiRunState"] = 1

            if index == "DubboInterface":
                varData["dubboRunState"] = 1

    varData["addBy"] = request.session.get("loginName")
    varData["serviceConfKey_id"] = varData["serviceConfKey"]
    del varData["serviceConfKey"]
    try:
        HttpConfService.httpConfAdd(varData)
    except Exception as e:
        return HttpResponse(ApiReturn(ApiReturn.CODE_GLOBAL_EXCEPITON,"key重复%s"%e).toJson())
    return HttpResponse(ApiReturn().toJson())


def userHttpConfEdit(request):
    varData = json.loads(parse.unquote(request.POST.get("data")))
    varData["addBy"] = request.session.get("loginName")
    getVar = user_http_confService.getUserHttpConf(varData["id"])
    if getVar.addBy.loginName != request.session.get("loginName"):
        return HttpResponse(ApiReturn(ApiReturn.CODE_GLOBAL_EXCEPITON, "只能修改自己的变量").toJson())
    user_http_confService.editUserHttpConf(varData)
    return HttpResponse(ApiReturn().toJson())

def addUserHttpConf(request):
    httpConfKey = request.POST.get("httpConfKey")
    loginName = request.session.get("loginName")
    userHttpConfCount = user_http_confService.queryUserHttpConfCount(loginName)
    if userHttpConfCount == 0:
        user_http_confService.addUserHttpConf(loginName,httpConfKey,0)
        return HttpResponse(ApiReturn().toJson())
    else:
        userCount = dbModelListToListDict(user_http_confService.queryUserHttpConfRepeat(loginName,httpConfKey))
        editLevel = dbModelListToListDict(user_http_confService.queryUserHttpConf(loginName))
        if len(userCount) == 0:
            for i in range(0,len(editLevel)):
                editLevel[i]["conflevel"] += 1
                editLevel[i]["modTime"] = datetime.datetime.now()
                user_http_confService.updateLevel(editLevel[i])
            user_http_confService.addUserHttpConf(loginName,httpConfKey,0)
            return HttpResponse(ApiReturn().toJson())
        elif userCount[0]["conflevel"] != 0:
            for i in range(0, len(editLevel)):
                editLevel[i]["conflevel"] = i+1
                editLevel[i]["modTime"] = datetime.datetime.now()
                user_http_confService.updateLevel(editLevel[i])
            userCount[0]["conflevel"] = 0
            userCount[0]["modTime"] = datetime.datetime.now()
            user_http_confService.updateLevel(userCount[0])
            return HttpResponse(ApiReturn().toJson())
        else:
            return HttpResponse(ApiReturn(ApiReturn.CODE_ERROR,"此配置已排在第一位").toJson())

@single_data_permission(TbUserHttpconf,TbUserHttpconf)
def delHttpConfKey(request):
    id = request.GET.get("id")
    HttpConfService.httpConfDel(id)
    return HttpResponse(ApiReturn().toJson())

@single_data_permission(TbConfigHttp,TbConfigHttp)
def httpConfSaveEdit(request):
    data = json.loads(parse.unquote(request.POST.get("data")))
    data["modTime"] = datetime.datetime.now()
    result = HttpConfService.httpConfEdit(data)
    return HttpResponse(ApiReturn().toJson())

def delAllUserHttpConf(request):
    user_http_confService.delAllUserHttpConf(request.session.get("loginName"))
    return HttpResponse(ApiReturn().toJson())