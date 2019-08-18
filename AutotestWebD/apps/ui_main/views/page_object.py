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

def showPOindex(request):
    langDict = getLangTextDict(request)
    context = {}

    context["uiPageObjectIndex"] = "current-page"
    context["userName"] = request.session.get("userName")
    if not isRelease:
        context["env"] = "test"
    # 文本
    text = {}
    text["pageTitle"] = langDict["ui"]["pageObjectMain"]
    text["subPageTitle"] = langDict["ui"]["pageObjectCheck"]

    context["text"] = text

    # context.update(getHttpConfForUI())
    context["page"] = 1
    return render(request, "ui_main/page_object/page_object_index.html", context)

def queryPageObjects(request):

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
        tbName = "tb3_ui_page_object"
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
    response = render(request, "ui_main/page_object/SubPages/page_object_list_subpage.html", context)
    return response

def addPOindex(request):
    langDict = getLangTextDict(request)
    context = {}

    context["uiPageObjectAdd"] = "current-page"
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
    # return render(request, "ui_main/page_object/page_object_add.html", context)
    return render(request, "ui_main/page_object/page_object_conf.html", context)


def queryPageObjectsList(request):

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
        tbName = "tb3_ui_page_object"
        versionCondition = ""
    else:
        tbName = "tb_version_global_vars"
        versionCondition = "and versionName='%s'" % request.session.get("version")

    # execSql = "SELECT g.*,u.userName FROM %s g LEFT JOIN tb_user u ON g.addBy = u.loginName WHERE 1=1 AND g.state=1 %s " % (tbName,versionCondition)
    execSql = "SELECT u.* from tb_ui_page_object u WHERE 1=1 "
    checkList = []
    for key in checkArr:
        if checkArr[key] == "":
            continue
        # elif key == "addBy":
        #     checkList.append("%%%s%%" % checkArr[key])
        #     checkList.append("%%%s%%" % checkArr[key])
        #     execSql += """ and (g.addBy LIKE %s or u.userName LIKE %s) """
        #
        #     continue
        checkList.append("%%%s%%" % checkArr[key])
        execSql += """ and g.%s """ % key
        execSql += """ LIKE %s"""
    execSql += """ ORDER BY %s""" % orderBy
    context = pagination(sqlStr=execSql, attrList=checkList, page=page, pageNum=commonWebConfig.testCasePageNum)
    context.update(getHttpConfForUI())
    response = render(request, "ui_main/page_object/subPages/page_object_add_subpage.html", context)
    return response

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


    execSql = "SELECT g.* from tb_ui_page_object g WHERE 1=1 "
    checkList = []
    for key in checkArr:
        if checkArr[key] == "":
            continue
        checkList.append("%%%s%%" % checkArr[key])
        execSql += """ and g.%s """ % key
        execSql += """ LIKE %s"""
    execSql += """ ORDER BY %s""" % orderBy
    print("execSql:", execSql)
    print("22222222222222222222")
    context = pagination(sqlStr=execSql, attrList=checkList, page=page, pageNum=commonWebConfig.testCasePageNum)
    print("33333333333333333333333")
    response = render(request, "ui_main/page_object/SubPages/page_object_conf_sub_page.html", context)
    return response