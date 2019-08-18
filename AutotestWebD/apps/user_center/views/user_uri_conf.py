from apps.common.func.CommonFunc import *
from django.db.models import Max
from apps.common.func.LanguageFunc import *
from django.shortcuts import render, HttpResponse
from all_models.models import *
from urllib import parse
from apps.user_center.services.user_uriService import user_uriService
from apps.common.config import commonWebConfig
from apps.config.services.serviceConfService import ServiceConfService
from apps.config.services.http_confService import HttpConfService
from apps.config.services.uriService import UriService
from apps.common.decorator.permission_normal_funcitons import *
import json

def userUriCheck(request):
    langDict = getLangTextDict(request)
    context = {}

    context["httpUserCenterURIConfPage"] = "current-page"
    context["userName"] = request.session.get("userName")
    if not isRelease:
        context["env"] = "test"
    # 文本
    text = {}
    text["pageTitle"] = langDict["web"]["httpUserCenterUserUriPageTitle"]
    text["subPageTitle"] = langDict["web"]["httpUserCenterUserUriSubPageTitle"]
    context["text"] = text
    context["page"] = 1
    context["uri"] = UriService.getUri(request, "ALL")
    context["title"] = "服务配置"

    return render(request, "InterfaceTest/user_center/user_uri_conf.html", context)

# def getUriData(request):
#     id = request.GET.get("id")
#     httpConfData = dbModelToDict(HttpConfService.getHttpConfForId(id))
#     httpConfList = httpConfData["httpConf"].split("\n")
#     result = []
#     loop = 0
#     for httpConfIndex in range (1,len(httpConfList)):
#         if httpConfList[httpConfIndex] == "" or "=" not in httpConfList[httpConfIndex]:
#             continue
#
#         indexData = httpConfList[httpConfIndex].split("=")
#         result.append({})
#         result[loop]["httpConfKey"] = indexData[0].strip()
#         result[loop]["httpConfValue"] = indexData[1].strip()
#
#         loop += 1
#     return HttpResponse(ApiReturn(body=result).toJson())

def queryUserUriConf(request):
    page = request.POST.get("page",1)
    if isInt(page):
        page = int(page)
    else:
        return HttpResponse("<script>alert('请验证页数参数');</script>")
    checkArr = json.loads(parse.unquote(request.POST.get("queryArr")))

    execSql = "SELECT s.*,tb_user.userName,muser.userName modByName FROM tb_config_uri s LEFT JOIN tb_user ON s.addBy=tb_user.loginName LEFT JOIN tb_user muser ON s.modBy=muser.loginName " \
              "LEFT JOIN (SELECT * FROM ( SELECT id ucid,uriKey uuUriKey,conflevel FROM tb_user_uri " \
              "WHERE addBy= '%s' ) b LEFT JOIN (SELECT uriKey cuUriKey FROM tb_config_uri) a ON b.uuUrikey = a.cuUriKey) c ON s.uriKey = c.cuUriKey  " \
              "WHERE s.state = 1" % request.session.get("loginName")
    checkList = []
    for key in checkArr:
        if checkArr[key] == "":
            continue
        if key == "addBy":
            checkList.append("%%%s%%" % checkArr[key])
            checkList.append("%%%s%%" % checkArr[key])
            execSql += """ and (s.addBy LIKE %s or tb_user.userName LIKE %s) """
            continue
        checkList.append("%%%s%%" % checkArr[key])
        execSql += """ and s.%s """ % key
        execSql += """ LIKE %s"""
    execSql += """ order by c.conflevel is null,c.conflevel ASC,s.modTime desc"""
    print(execSql)
    context = pagination(execSql, checkList, page, commonWebConfig.userHttpConfPageNum,request=request)
    context["uriServices"] = UriService.getUri(request)
    context["dubboServices"] = dbModelListToListDict(TbConfigUri.objects.filter(state=1, protocol="DUBBO").order_by("level"))
    response = render(request, "InterfaceTest/user_center/SubPages/user_uri_conf_sub_page.html", context)
    return response

def addUserUriSort(request):
    uriKey = request.POST.get("uriKey")
    loginName = request.session.get("loginName")
    userUriCount = user_uriService.queryUserUriCount(loginName)
    if userUriCount == 0:
        user_uriService.addUserUrl(loginName,uriKey,0)
        return HttpResponse(ApiReturn().toJson())
    else:
        userCount = dbModelListToListDict(user_uriService.queryUserUriRepeat(loginName,uriKey))
        editLevel = dbModelListToListDict(user_uriService.queryUserUri(loginName))
        if len(userCount) == 0:
            for i in range(0,len(editLevel)):
                editLevel[i]["conflevel"] += 1
                editLevel[i]["modTime"] = datetime.datetime.now()
                user_uriService.updateLevel(editLevel[i])
            user_uriService.addUserUrl(loginName,uriKey,0)
            return HttpResponse(ApiReturn().toJson())
        elif userCount[0]["conflevel"] != 0:
            for i in range(0, len(editLevel)):
                editLevel[i]["conflevel"] = i+1
                editLevel[i]["modTime"] = datetime.datetime.now()
                user_uriService.updateLevel(editLevel[i])
            userCount[0]["conflevel"] = 0
            userCount[0]["modTime"] = datetime.datetime.now()
            user_uriService.updateLevel(userCount[0])
            return HttpResponse(ApiReturn().toJson())
        else:
            return HttpResponse(ApiReturn(ApiReturn.CODE_EXCEPTION,"此配置已排在第一位").toJson())

@single_data_permission(TbConfigUri,TbConfigUri)
def addUserUriApply(request):
    alias = request.POST.get("alias")
    protocols = request.POST.get("protocols")
    loginName = request.session.get("loginName")
    failedProtocol = ""
    for tmpProtocol in protocols.split(","):
        if tmpProtocol.strip() != "":
            try:
                try:
                    id = TbConfigUri.objects.all().aggregate(Max('id'))["id__max"] + 1
                except:
                    id = 1
                tmpUriModel = TbConfigUri()
                uriKey = "%s-%s" % (tmpProtocol.strip().lower(),alias)
                protocol = tmpProtocol.strip()
                if protocol == "HTTP":
                    uriAlias = alias
                else:
                    uriAlias = "%s(%s)" % (alias,tmpProtocol.strip().lower())

                oldData = TbConfigUri.objects.filter(uriKey=uriKey)
                if len(oldData) > 0:
                    data = oldData[0]
                    data.state = 1
                    data.save()
                else:

                    tmpUriModel.id = id
                    tmpUriModel.alias = uriAlias
                    tmpUriModel.uriDesc = "%s的%s服务" % (uriKey,tmpProtocol)
                    tmpUriModel.uriKey = uriKey
                    tmpUriModel.protocol = protocol
                    tmpUriModel.addBy = loginName
                    tmpUriModel.save(force_insert=True)
            except Exception as e:
                print(traceback.format_exc())
                failedProtocol += tmpProtocol.strip()+" "

    if failedProtocol == "":
        return HttpResponse(ApiReturn(code=ApiReturn.CODE_OK,message="添加成功！").toJson())
    else:
        return HttpResponse(ApiReturn(code=ApiReturn.CODE_ERROR,message="协议%s添加失败！" % failedProtocol).toJson())

@single_data_permission(TbConfigUri,TbConfigUri)
def saveUriEdit(request):
    uriKey = request.POST.get("uriKey")
    httpConfDesc = request.POST.get("httpConfDesc")
    loginName = request.session.get("loginName")
    TbConfigUri.objects.filter(uriKey=uriKey).update(uriDesc=httpConfDesc,modBy=loginName,modTime=get_current_time())
    return HttpResponse(ApiReturn(code=ApiReturn.CODE_OK,message="修改成功！").toJson())

@single_data_permission(TbConfigUri,TbConfigUri)
def delUri(request):
    uriKey = request.GET.get("uriKey")
    loginName = request.session.get("loginName")
    TbConfigUri.objects.filter(uriKey=uriKey).update(state=0,modBy=loginName,modTime=get_current_time())
    return HttpResponse(ApiReturn(code=ApiReturn.CODE_OK,message="删除成功！").toJson())


def userEnvUriCheck(request):
    langDict = getLangTextDict(request)
    context = {}

    context["httpUserCenterEnvURIConfPage"] = "current-page"
    context["userName"] = request.session.get("userName")
    if not isRelease:
        context["env"] = "test"
    # 文本
    text = {}
    text["pageTitle"] = "请求地址配置"
    text["subPageTitle"] = "请求地址查看"
    context["text"] = text
    context["page"] = 1
    context["envConfList"] = HttpConfService.getAllHttpConf(request)
    context["uri"] = UriService.getUri(request,"ALL")
    context["title"] = "请求地址配置"

    return render(request, "InterfaceTest/user_center/user_env_uri_conf.html", context)

def queryUserEnvUriConf(request):
    page = request.POST.get("page")
    if isInt(page):
        page = int(page)
    else:
        return HttpResponse("<script>alert('请验证页数参数');</script>")
    checkArr = json.loads(parse.unquote(request.POST.get("queryArr")))

    execSql = "SELECT s.*,tb_user.userName,curi.protocol protocol,muser.userName modByName FROM tb_env_uri_conf s LEFT JOIN tb_user ON s.addBy=tb_user.loginName  LEFT JOIN tb_user muser ON s.modBy=muser.loginName " \
              "LEFT JOIN tb_config_http chttp ON s.httpConfKey=chttp.httpConfKey " \
              "LEFT JOIN tb_config_uri curi ON s.uriKey=curi.uriKey " \
              "WHERE s.state = 1"
    checkList = []
    for key in checkArr:
        if checkArr[key] == "":
            continue
        if key == "addBy":
            checkList.append("%%%s%%" % checkArr[key])
            checkList.append("%%%s%%" % checkArr[key])
            execSql += """ and (s.addBy LIKE %s or tb_user.userName LIKE %s) """
            continue
        if key == "protocol":
            checkList.append("%s" % checkArr[key])
            execSql += """ and curi.%s """ % key
            execSql += """ = %s"""
            continue
        if key in ["httpConfKey","uriKey"]:
            checkList.append("%s" % checkArr[key])
            execSql += """ and s.%s """ % key
            execSql += """ = %s"""
            continue
        checkList.append("%%%s%%" % checkArr[key])
        execSql += """ and s.%s """ % key
        execSql += """ LIKE %s"""
    execSql += """ order by s.modTime DESC"""
    context = pagination(execSql, checkList, page, commonWebConfig.userHttpConfPageNum,request=request)
    # context["uriServices"] = UriService.getUri(request)
    # context["dubboServices"] = dbModelListToListDict(TbConfigUri.objects.filter(state=1, protocol="DUBBO").order_by("level"))
    response = render(request, "InterfaceTest/user_center/SubPages/env_uri_conf_sub_page.html", context)
    return response

@single_data_permission(TbEnvUriConf,TbEnvUriConf)
def delEnvUri(request):
    id = request.GET.get("id")
    TbEnvUriConf.objects.filter(id=id).update(state=0)
    return HttpResponse(ApiReturn().toJson())

@single_data_permission(TbEnvUriConf,TbEnvUriConf)
def saveEditEnvUri(request):
    id = request.POST.get("id")
    requestAddr = request.POST.get("requestAddr")
    TbEnvUriConf.objects.filter(id=id).update(requestAddr=requestAddr,modBy=request.session.get("loginName"),state=1)
    return HttpResponse(ApiReturn().toJson())

@single_data_permission(TbEnvUriConf,TbEnvUriConf)
def saveEnvUri(request):
    requestAddr = request.POST.get("requestAddr")
    httpConfKey = request.POST.get("httpConfKey")
    uriKey = request.POST.get("uriKey")
    envUri = TbEnvUriConf.objects.filter(httpConfKey = httpConfKey,uriKey=uriKey)
    if(envUri):
        if envUri[0].state == 1:
            #提示错误
            return HttpResponse(ApiReturn(code=ApiReturn.CODE_ERROR,message="已经存在的请求配置，不能重复添加，请编辑！").toJson())
        elif envUri[0].state == 0:
            #进行更新
            envUri[0].state = 1
            envUri[0].requestAddr = requestAddr
            envUri[0].addBy = request.session.get("loginName")
            envUri[0].addTime = get_current_time()
            envUri[0].save(force_update=True)
            return HttpResponse(ApiReturn(message="添加成功！").toJson())
    else:
        #进行add
        teuri = TbEnvUriConf()
        teuri.requestAddr = requestAddr
        teuri.httpConfKey = httpConfKey
        teuri.uriKey = uriKey
        teuri.addBy = request.session.get("loginName")
        teuri.save(force_insert=True)
        return HttpResponse(ApiReturn(message="添加成功！！").toJson())

def delAllUserUri(request):
    TbUserUri.objects.filter(addBy=request.session.get("loginName")).delete()
    return HttpResponse(ApiReturn().toJson())