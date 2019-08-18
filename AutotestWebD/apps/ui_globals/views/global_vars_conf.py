from apps.common.func.LanguageFunc import *
from urllib import parse
from apps.common.config import commonWebConfig
from apps.ui_globals.services.global_varsService import global_varsService
from apps.common.func.WebFunc import *
import json
from apps.version_manage.services.common_service import VersionService
from apps.config.services.http_confService import HttpConfService

def globalVarsCheck(request):
    langDict = getLangTextDict(request)
    context = {}

    context["uiUserCenterGlobalVarsPage"] = "current-page"
    context["userName"] = request.session.get("userName")
    if not isRelease:
        context["env"] = "test"

    context.update(getHttpConfForUI())
    # 文本
    text = {}
    text["pageTitle"] = langDict["web"]["httpUserCenterGlobalVarsPageTitle"]
    text["subPageTitle"] = langDict["web"]["httpUserCenterGlobalVarsSubPageTitle"]
    context["text"] = text
    context["page"] = 1
    return render(request, "ui_globals/global_vars_conf.html", context)


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
        tbName = "tb3_ui_global_vars"
        versionCondition = ""
    else:
        tbName = "tb_version_global_vars"
        versionCondition = "and versionName='%s'" % request.session.get("version")

    execSql = "SELECT g.*,u.userName FROM %s g LEFT JOIN tb_user u ON g.addBy = u.loginName WHERE 1=1 AND g.state=1 %s " % (tbName,versionCondition)
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
    response = render(request, "ui_globals/SubPages/global_vars_conf_sub_page.html", context)
    return response

def varsConfDel(request):
    id = request.GET.get("id")
    if VersionService.isCurrentVersion(request):
        getVar = global_varsService.getVar(id)
        if getVar.addBy != request.session.get("loginName"):
            return HttpResponse(ApiReturn(ApiReturn.CODE_GLOBAL_EXCEPITON,"只能删除自己的变量").toJson())

        try:
            global_varsService.delVar(id)
            return HttpResponse(ApiReturn(ApiReturn.CODE_OK).toJson())
        except Exception as e:
            return HttpResponse(ApiReturn(ApiReturn.CODE_GLOBAL_EXCEPITON,e).toJson())
    else:
        getVar = global_varsService.getVersionVar(id)
        if getVar.addBy.loginName != request.session.get("loginName"):
            return HttpResponse(ApiReturn(ApiReturn.CODE_GLOBAL_EXCEPITON, "只能删除自己的变量").toJson())

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

    httpConfList = HttpConfService.queryUIRunHttpConfSort(request)
    varData["httpConf"] = {}
    varData["httpConf"]["common"] = substr(varData["varValue"], "[CONF=common]", "[ENDCONF]")
    for i in range(0, len(httpConfList)):
        if httpConfList[i]["httpConfKey"] not in varData["varValue"]:
            varData["httpConf"]["%s" % httpConfList[i]["httpConfKey"]] = ""
            continue
        varData["httpConf"]["%s" % httpConfList[i]["httpConfKey"]] = substr(varData["varValue"],"[CONF=%s]" % httpConfList[i]["httpConfKey"],"[ENDCONF]")
    return HttpResponse(ApiReturn(body=varData).toJson())

def varsConfAdd(request):
    varData = json.loads(parse.unquote(request.POST.get("data")))
    varData["addBy"] = request.session.get("loginName")
    try:
        if VersionService.isCurrentVersion(request):
            global_varsService.addVar(varData)
        else:
            global_varsService.addVersionVar(varData,VersionService.getVersionName(request))
    except Exception as e:
        return HttpResponse(ApiReturn(ApiReturn.CODE_GLOBAL_EXCEPITON,"key重复").toJson())
    return HttpResponse(ApiReturn().toJson())

def varsConfEdit(request):
    varData = json.loads(parse.unquote(request.POST.get("data")))
    if VersionService.isCurrentVersion(request):
        getVar = global_varsService.getVar(varData["id"])
        if getVar.addBy != request.session.get("loginName"):
            return HttpResponse(ApiReturn(ApiReturn.CODE_GLOBAL_EXCEPITON, "只能修改自己的变量").toJson())
        global_varsService.editVar(varData)
        return HttpResponse(ApiReturn().toJson())
    else:
        getVar = global_varsService.getVersionVar(varData["id"])
        if getVar.addBy.loginName != request.session.get("loginName"):
            return HttpResponse(ApiReturn(ApiReturn.CODE_GLOBAL_EXCEPITON, "只能修改自己的变量").toJson())
        global_varsService.editVersionVar(varData,VersionService.getVersionName(request))
        return HttpResponse(ApiReturn().toJson())