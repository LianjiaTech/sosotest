from apps.common.func.CommonFunc import *
from apps.common.func.LanguageFunc import *
from django.shortcuts import render, HttpResponse
from urllib import parse
from apps.common.config import commonWebConfig
from apps.common.func.WebFunc import *
from apps.ui_globals.services.global_textService import global_textService
from apps.config.services.serviceConfService import ServiceConfService
import json
from apps.version_manage.services.common_service import VersionService

def globalTextCheck(request):
    langDict = getLangTextDict(request)
    context = {}

    context["uiUserCenterGlobalTextPage"] = "current-page"
    context["userName"] = request.session.get("userName")
    if not isRelease:
        context["env"] = "test"
    # 文本
    text = {}
    text["pageTitle"] = langDict["web"]["httpUserCenterGlobalTextPageTitle"]
    text["subPageTitle"] = langDict["web"]["httpUserCenterGlobalTextSubPageTitle"]

    context["text"] = text

    context.update(getHttpConfForUI())
    context["page"] = 1
    return render(request, "ui_globals/global_text_conf.html", context)


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
        tbName = "tb3_ui_global_text"
        versionCondition = ""
    else:
        tbName = "tb_version_global_text"
        versionCondition = "and versionName='%s'" % request.session.get("version")

    execSql = "SELECT g.*,u.userName FROM %s g LEFT JOIN tb_user u ON g.addBy = u.loginName WHERE 1=1 AND g.state=1 %s" %(tbName,versionCondition)
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
    context = pagination(sqlStr=execSql, attrList=checkList, page=page, pageNum=commonWebConfig.testCasePageNum)
    context.update(getHttpConfForUI())
    response = render(request, "ui_globals/SubPages/global_text_conf_sub_page.html", context)
    return response

def textConfDel(request):
    id = request.GET.get("id")
    if VersionService.isCurrentVersion(request):
        getText = global_textService.getText(id)
        if getText.addBy != request.session.get("loginName"):
            return HttpResponse(ApiReturn(ApiReturn.CODE_GLOBAL_EXCEPITON,"只能删除自己的变量").toJson())
        try:
            global_textService.delText(id)
            return HttpResponse(ApiReturn(ApiReturn.CODE_OK).toJson())
        except Exception as e :
            return HttpResponse(ApiReturn(ApiReturn.CODE_GLOBAL_EXCEPITON,e).toJson())
    else:
        getText = global_textService.getVersionText(id)
        #addBy不是fk了
        if getText.addBy != request.session.get("loginName"):
            return HttpResponse(ApiReturn(ApiReturn.CODE_GLOBAL_EXCEPITON,"只能删除自己的变量").toJson())
        try:
            global_textService.delVersionText(id)
            return HttpResponse(ApiReturn(ApiReturn.CODE_OK).toJson())
        except Exception as e :
            return HttpResponse(ApiReturn(ApiReturn.CODE_GLOBAL_EXCEPITON,e).toJson())

def textConfAdd(request):
    TextData = json.loads(parse.unquote(request.POST.get("data")))
    TextData["addBy"] = request.session.get("loginName")
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

def textConfEdit(request):
    TextData = json.loads(parse.unquote(request.POST.get("data")))
    if VersionService.isCurrentVersion(request):
        getText = global_textService.getText(TextData["id"])
        if getText.addBy != request.session.get("loginName"):
            return HttpResponse(ApiReturn(ApiReturn.CODE_GLOBAL_EXCEPITON, "只能修改自己的变量").toJson())
        global_textService.editText(TextData)
        return HttpResponse(ApiReturn().toJson())
    else:
        getText = global_textService.getVersionText(TextData["id"])
        if getText.addBy != request.session.get("loginName"):
            return HttpResponse(ApiReturn(ApiReturn.CODE_GLOBAL_EXCEPITON, "只能修改自己的变量").toJson())
        global_textService.editVersionText(TextData,VersionService.getVersionName(request))
        return HttpResponse(ApiReturn().toJson())

def getTextConf(request):
    id = request.GET.get("id")
    if VersionService.isCurrentVersion(request):
        varData = dbModelToDict(global_textService.getText(id))
    else:
        varData = dbModelToDict(global_textService.getVersionText(id))

    httpConfList = HttpConfService.queryUIRunHttpConfSort(request)
    varData["httpConf"] = {}
    varData["httpConf"]["common"] = substr(varData["textValue"], "[CONF=common]", "[ENDCONF]")
    for i in range(0, len(httpConfList)):
        if httpConfList[i]["httpConfKey"] not in varData["textValue"]:
            varData["httpConf"]["%s" % httpConfList[i]["httpConfKey"]] = ""
            continue
        varData["httpConf"]["%s" % httpConfList[i]["httpConfKey"]] = substr(varData["textValue"],"[CONF=%s]" % httpConfList[i]["httpConfKey"],"[ENDCONF]")

    return HttpResponse(ApiReturn(body=varData).toJson())