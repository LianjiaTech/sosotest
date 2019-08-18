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
    text["pageTitle"] = "数据环境"
    text["subPageTitle"] = "数据环境配置查看"
    context["text"] = text
    serviceConf = ServiceConfService.getServiceConf()
    context["services"] = serviceConf
    context["uriServices"] = UriService.getUri(request)
    context["dubboServices"] = dbModelListToListDict(TbConfigUri.objects.filter(state=1,protocol="DUBBO").order_by("level"))
    context["page"] = 1
    context["title"] = "数据服务"

    return render(request, "InterfaceTest/user_center/user_service_conf.html", context)

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

    execSql = "SELECT c.* FROM tb_config_service c WHERE 1=1 AND c.state=1 "
    checkList = []
    for key,value in checkArr.items():
        if value != "":
            checkList.append("%%%s%%" % checkArr[key])
            execSql += """ and c.%s """ % key
            execSql += """ LIKE %s"""
    context = pagination(execSql, checkList, page, commonWebConfig.userHttpConfPageNum)
    #处理掉username和password
    for tmpData in context["pageDatas"]:
        # tmpData["serviceConf"] = re.sub(r',\s(.*)"username(.*)\n\s(.*)', '', tmpData["serviceConf"]+"\n")
        # tmpData["serviceConf"] = re.sub(r',(.*)\s(.*)"password(.*)\n\s(.*)', '', tmpData["serviceConf"]+"\n").strip()

        tmpServiceConfStr = ""
        serviceDict = json.loads(tmpData["serviceConf"])
        for tmpkey,tmpvalue in serviceDict.items():
            tmpServiceConfStr += "%s:\n" % tmpkey
            for tmpSingleKey,tmpSingleValue in tmpvalue.items():
                if "comment" in tmpSingleValue.keys():
                    tmpServiceConfStr += "# %s\n" % tmpSingleValue["comment"]
                tmpServiceConfStr += "%s => %s:%s\n\n" % (tmpSingleKey,tmpSingleValue["host"],tmpSingleValue["port"])

            tmpServiceConfStr += "\n"
        tmpData["serviceConf"] = tmpServiceConfStr

    context["uriServices"] = UriService.getUri(request)
    context["dubboServices"] = dbModelListToListDict(TbConfigUri.objects.filter(state=1,protocol="DUBBO").order_by("level"))
    response = render(request, "InterfaceTest/user_center/SubPages/user_service_conf_sub_page.html", context)
    return response

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

def delHttpConfKey(request):
    httpConfKey = request.GET.get("httpConfKey")
    HttpConfService.httpConfDel(httpConfKey)
    return HttpResponse(ApiReturn().toJson())


def httpConfSaveEdit(request):
    data = json.loads(parse.unquote(request.POST.get("data")))
    data["modTime"] = datetime.datetime.now()
    result = HttpConfService.httpConfEdit(data)
    return HttpResponse(ApiReturn().toJson())