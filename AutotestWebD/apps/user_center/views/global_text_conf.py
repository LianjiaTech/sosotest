from apps.common.func.CommonFunc import *
from apps.common.func.LanguageFunc import *
from django.shortcuts import render, HttpResponse
from urllib import parse
from apps.common.config import commonWebConfig
from apps.common.func.WebFunc import getServiceConf
from apps.user_center.services.global_textService import global_textService
from apps.config.services.serviceConfService import ServiceConfService
import json
from apps.version_manage.services.common_service import VersionService
from django.views.decorators.csrf import csrf_exempt
from apps.common.decorator.permission_normal_funcitons import *


def globalTextCheck(request):
    langDict = getLangTextDict(request)
    context = {}

    context["httpUserCenterGlobalTextPage"] = "current-page"
    context["userName"] = request.session.get("userName")
    if not isRelease:
        context["env"] = "test"
    # 文本
    text = {}
    text["pageTitle"] = langDict["web"]["httpUserCenterGlobalTextPageTitle"]
    text["subPageTitle"] = langDict["web"]["httpUserCenterGlobalTextSubPageTitle"]

    context["text"] = text
    context["title"] = "组合文本"

    context.update(getServiceConf(request))
    context["page"] = 1
    return render(request, "InterfaceTest/user_center/global_text_conf.html", context)


def queryText(request):

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
        tbName = "tb_global_text"
        versionCondition = ""
    else:
        tbName = "tb_version_global_text"
        versionCondition = "and versionName='%s'" % request.session.get("version")

    execSql = "SELECT g.*,u.userName,umod.userName modByName  FROM %s g LEFT JOIN tb_user u ON g.addBy = u.loginName LEFT JOIN tb_user umod ON g.modBy = umod.loginName  WHERE g.state=1 %s" %(tbName,versionCondition)
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
    response = render(request, "InterfaceTest/user_center/SubPages/global_text_conf_sub_page.html", context)
    return response

@single_data_permission(TbGlobalText,TbVersionGlobalText)
def textConfDel(request):
    id = request.GET.get("id")
    if VersionService.isCurrentVersion(request):
        getText = global_textService.getText(id)
        if getText.addBy.loginName != request.session.get("loginName"):
            changeLog = TbUserChangeLog()
            changeLog.version = request.session.get("version")
            changeLog.loginName = request.session.get("loginName")
            changeLog.otherLoginName = getText.addBy.loginName
            changeLog.type = 0
            changeLog.beforeChangeData = dictToJson(dbModelToDict(getText))
            changeLog.dataId = getText.textKey
            changeLog.changeDataId = getText.textKey
            changeLog.save()
        try:
            global_textService.delText(id)
            return HttpResponse(ApiReturn(ApiReturn.CODE_OK).toJson())
        except Exception as e :
            return HttpResponse(ApiReturn(ApiReturn.CODE_GLOBAL_EXCEPITON,e).toJson())
    else:
        getText = global_textService.getVersionText(id)
        if getText.addBy.loginName != request.session.get("loginName"):
            changeLog = TbUserChangeLog()
            changeLog.version = request.session.get("version")
            changeLog.loginName = request.session.get("loginName")
            changeLog.otherLoginName = getText.addBy.loginName
            changeLog.type = 0
            changeLog.beforeChangeData = dictToJson(dbModelToDict(getText))
            changeLog.dataId = getText.textKey
            changeLog.changeDataId = getText.textKey
            changeLog.save()
        try:
            global_textService.delVersionText(id)
            return HttpResponse(ApiReturn(ApiReturn.CODE_OK).toJson())
        except Exception as e :
            return HttpResponse(ApiReturn(ApiReturn.CODE_GLOBAL_EXCEPITON,e).toJson())

@single_data_permission(TbGlobalText,TbVersionGlobalText)
def textConfAdd(request):
    TextData = json.loads(parse.unquote(request.POST.get("data")))
    TextData["addBy_id"] = request.session.get("loginName")
    if VersionService.isCurrentVersion(request):
        try:
            global_textService.addText(TextData)
        except Exception as e:
            return HttpResponse(ApiReturn(ApiReturn.CODE_GLOBAL_EXCEPITON,"key重复").toJson())
        return HttpResponse(ApiReturn().toJson())
    else:
        try:
            global_textService.addVersionText(TextData,VersionService.getVersionName(request))
        except Exception as e:
            return HttpResponse(ApiReturn(ApiReturn.CODE_GLOBAL_EXCEPITON,"key重复").toJson())
        return HttpResponse(ApiReturn().toJson())

@single_data_permission(TbGlobalText,TbVersionGlobalText)
def textConfEdit(request):
    TextData = json.loads(parse.unquote(request.POST.get("data")))
    TextData["modBy"] = request.session.get("loginName")
    if VersionService.isCurrentVersion(request):
        getText = global_textService.getText(TextData["id"])
        if getText.addBy.loginName != request.session.get("loginName"):
            changeLog = TbUserChangeLog()
            changeLog.version = request.session.get("version")
            changeLog.loginName = request.session.get("loginName")
            changeLog.otherLoginName = getText.addBy.loginName
            changeLog.type = 1
            changeLog.beforeChangeData = dictToJson(dbModelToDict(getText))
            changeLog.afterChangeData = dictToJson(TextData)
            changeLog.dataId = getText.textKey
            changeLog.changeDataId = getText.textKey
            changeLog.save()
        global_textService.editText(TextData)
        return HttpResponse(ApiReturn().toJson())
    else:
        getText = global_textService.getVersionText(TextData["id"])
        if getText.addBy.loginName != request.session.get("loginName"):
            changeLog = TbUserChangeLog()
            changeLog.version = request.session.get("version")
            changeLog.loginName = request.session.get("loginName")
            changeLog.otherLoginName = getText.addBy.loginName
            changeLog.type = 1
            changeLog.beforeChangeData = dictToJson(dbModelToDict(getText))
            changeLog.afterChangeData = dictToJson(TextData)
            changeLog.dataId = getText.textKey
            changeLog.changeDataId = getText.textKey
            changeLog.save()
        global_textService.editVersionText(TextData,VersionService.getVersionName(request))
        return HttpResponse(ApiReturn().toJson())

def getTextConf(request):
    id = request.GET.get("id")
    if VersionService.isCurrentVersion(request):
        varData = dbModelToDict(global_textService.getText(id))
    else:
        varData = dbModelToDict(global_textService.getVersionText(id))

    serviceConf = ServiceConfService.queryServiceConfSort(request)
    varData["serviceConf"] = {}
    varData["serviceConf"]["common"] = substr(varData["textValue"], "[CONF=common]", "[ENDCONF]")
    for i in range(0, len(serviceConf)):
        if serviceConf[i]["serviceConfKey"] not in varData["textValue"]:
            varData["serviceConf"]["%s" % serviceConf[i]["serviceConfKey"]] = ""
            continue
        varData["serviceConf"]["%s" % serviceConf[i]["serviceConfKey"]] = substr(varData["textValue"],"[CONF=%s]" % serviceConf[i]["serviceConfKey"],"[ENDCONF]")
    return HttpResponse(ApiReturn(body=varData).toJson())


@csrf_exempt
def getGlobalTextForVarKey(request):
    textKey = request.GET.get("textKey",None)
    token = request.GET.get("token",None)

    if textKey == None:
        return HttpResponse(ApiReturn(ApiReturn.CODE_ERROR,message="参数textKey 不能为空").toJson())

    if token == None:
        return HttpResponse(ApiReturn(ApiReturn.CODE_ERROR,message="参数token 不能为空").toJson())

    getUser = TbUser.objects.filter(token=token,state=1)
    if len(getUser) == 0:
        return HttpResponse(ApiReturn(ApiReturn.CODE_ERROR, message="参数token 查询用户错误").toJson())

    getText = TbGlobalText.objects.filter(textKey=textKey,state=1)
    if len(getText) == 0:
        return HttpResponse(ApiReturn(ApiReturn.CODE_ERROR, message="参数varKey 查询全局变量错误").toJson())
    serviceConfList = ServiceConfService.getServiceConf()
    textData = getText.last().textValue
    retVar = {}
    if "[CONF=common]" in textData:
        retVar["common"] = substr(textData,"[CONF=common]","[ENDCONF]")
    for serviceIndex in serviceConfList:
        if "[CONF=%s]" % serviceIndex["serviceConfKey"] not in textData:
            continue
        retVar[serviceIndex["serviceConfKey"]] = substr(textData,"[CONF=%s]" % serviceIndex["serviceConfKey"],"[ENDCONF]")

    return HttpResponse(ApiReturn(ApiReturn.CODE_OK, body=retVar).toJson())

@csrf_exempt
def setGlobalTextForVarKey(request):
    textKey = request.POST.get("textKey", None)
    token = request.POST.get("token", None)
    textValue = request.POST.get("textValue", None)

    if textKey == None:
        return HttpResponse(ApiReturn(ApiReturn.CODE_ERROR, message="参数textKey 不能为空").toJson())

    if token == None:
        return HttpResponse(ApiReturn(ApiReturn.CODE_ERROR, message="参数token 不能为空").toJson())

    getUser = TbUser.objects.filter(token=token, state=1)
    if len(getUser) == 0:
        return HttpResponse(ApiReturn(ApiReturn.CODE_ERROR, message="参数token 查询用户错误").toJson())

    getText = TbGlobalText.objects.filter(textKey=textKey, state=1)
    if len(getText) == 0:
        return HttpResponse(ApiReturn(ApiReturn.CODE_ERROR, message="参数varKey 查询全局变量错误").toJson())
    if type(textValue) == type(""):
        if not isJson(textValue):
            return HttpResponse(ApiReturn(ApiReturn.CODE_ERROR, message="参数varValue不是JSON格式").toJson())
        textDict = json.loads(textValue)
    elif type(textValue) == type({}):
        textDict = textValue
    else:
        return HttpResponse(ApiReturn(ApiReturn.CODE_ERROR, message="参数varValue不是JSON格式").toJson())
    serviceConfList = ServiceConfService.getServiceConf()
    serviceList = []
    for serviceIndex in serviceConfList:
        serviceList.append(serviceIndex["serviceConfKey"])

    textText = ""
    for index in textDict:
        if index !="common" and index not in serviceList:
            print(index)
            return HttpResponse(ApiReturn(ApiReturn.CODE_ERROR,"varValue中存在Key不为HTTPConfKey").toJson())
        textText += "[CONF=%s]%s[ENDCONF]" % (index,textDict[index])
    varData = getText.last()
    varData.textValue = textText
    varData.modBy = getUser.last().loginName
    varData.save()


    return HttpResponse(ApiReturn(ApiReturn.CODE_OK).toJson())