from urllib import parse
from apps.common.config import commonWebConfig
from apps.common.func.LanguageFunc import *
from apps.common.model.RedisDBConfig import *
from apps.data_keyword.services.main_service import MainService
from django.shortcuts import render,HttpResponse,redirect
from apps.config.services.businessLineService import *
from apps.config.services.modulesService import *
from apps.common.func.WebFunc import addUserLog
from apps.common.func.ExecFunc import *
from apps.common.decorator.permission_normal_funcitons import *
from all_models_for_mock.models import Tb4DataKeyword

retmsg = ""
logger = logging.getLogger("django")


def listPage(request):
    request.session['groupLevel1'] = groupLevel1
    request.session['groupLevel2'] = groupLevel2
    request.session['isReleaseEnv'] = isRelease

    langDict = getLangTextDict(request)
    context = {}
    if not isRelease:
        context["env"] = "test"
    context["datakeywordList"] = "current-page"
    context["userName"] = request.session.get("userName")
    context["checkBusinessLine"] = dbModelListToListDict(BusinessService.getAllBusinessLine())
    context["checkModules"] = dbModelListToListDict(ModulesService.getAllModules())
    # 文本
    text = {}
    text["pageTitle"] = "数据关键字/PYTHON模式"
    context["text"] = text
    context["page"] = 1
    # context["lang"] = getLangTextDict(request)
    addUserLog(request, "DataKeyword管理->查看->页面展示->成功", "PASS")
    context["title"] = "KEYWORD/PYTHON"
    return render(request, "data_keyword/list.html", context)

def listData(request):
    page = request.POST.get("page")
    if isInt(page):
        page = int(page)
    else:
        addUserLog(request, "DataKeyword管理->查看用例->获取数据->页面参数不合法", "FAIL")
        return HttpResponse("<script>alert('请验证页数参数');</script>")
    checkArr = json.loads(parse.unquote(request.POST.get("checkArr")))

    orderBy = request.POST.get("orderBy")
    if isSqlInjectable(orderBy):
        addUserLog(request, "DataKeyword管理->查看用例->获取数据->SQL注入检测时发现查询条件非法", "FAIL")
        return HttpResponse("<script>alert('查询条件非法');</script>")

    tbName = "tb4_data_keyword"
    versionCondition = ""

    execSql = "SELECT i.*,u.userName,mu.userName modByName from %s i LEFT JOIN tb_user mu ON i.modBy = mu.loginName LEFT JOIN tb_user u ON i.addBy = u.loginName  WHERE 1=1 and i.state=1 %s" % (
    tbName, versionCondition)
    print(execSql)
    checkList = []
    for key in checkArr:
        if checkArr[key] == "":
            continue
        elif key == "caseFounder":
            checkList.append("%%%s%%" % checkArr[key])
            checkList.append("%%%s%%" % checkArr[key])
            execSql += """ and (i.addBy LIKE %s or u.userName LIKE %s) """
            continue
        elif key == "module":
            checkList.append("%%%s%%" % checkArr[key])
            execSql += """ and m.moduleName LIKE %s """
            continue
        elif key == "businessLine":
            checkList.append("%%%s%%" % checkArr[key])
            execSql += """ and b.bussinessLineName LIKE %s """
            continue
        checkList.append("%%%s%%" % checkArr[key])
        execSql += """ and i.%s """ % key
        execSql += """ LIKE %s"""
    execSql += """ ORDER BY %s""" % orderBy
    otherUserList = []
    context = pagination(sqlStr=execSql, attrList=checkList, page=page, pageNum=commonWebConfig.interFacePageNum,request=request)
    for index in context["pageDatas"]:
        if index["addBy"] not in otherUserList:
            otherUserList.append(index["addBy"])


    response = render(request, "data_keyword/SubPages/list_data.html", context)
    addUserLog(request, "DataKeyword管理->查看->获取数据->成功", "PASS")
    return response

@single_add_page_permission
def addPage(request,context):
    context["option"] = "add"
    context["datakeywordAdd"] = "current-page"
    if not isRelease:
        context["env"] = "test"
    # 文本
    text = {}
    if request.GET.get("type","DATA_KEYWORD") == "DATA_KEYWORD":
        context["title"] = "添加自定义关键字"
        text["pageTitle"] = "自定义关键字"
        text["subPageTitle"] = "添加自定义关键字"
    else:
        context["title"] = "添加PYTHON代码"
        text["pageTitle"] = "PYTHON代码"
        text["subPageTitle"] = "添加PYTHON代码"

    context["text"] = text

    context["importStr"] = getPythonThirdLib()
    addUserLog(request, "DataKeyword管理->添加->页面展示->成功", "PASS")
    return render(request, "data_keyword/add.html", context)

@single_data_permission(Tb4DataKeyword,Tb4DataKeyword)
def addData(request):
    # 当前版本使用历史代码，不更新。
    if request.method != 'POST':
        return HttpResponse(ApiReturn(ApiReturn.CODE_METHOD_ERROR, "请求方式错误", "").toJson())
    data = json.loads(request.POST.get("postData"))
    try:
        retCode,retValue = MainService.addData(data, request.session.get("loginName"))
        return HttpResponse(ApiReturn(retCode, retValue, "").toJson())
    except Exception as e:
        logger.error(traceback.format_exc())
        return HttpResponse(ApiReturn(ApiReturn.CODE_INTERFACE_ERROR, "添加dataKeyword错误", "Failed: %s" % e).toJson())

def operationCheckByKey(request):
   try:
        key = request.GET.get("key")
        interObj = MainService.getDataByKey(key)
        return redirect("/datakeyword/operationCheck?id=%s&option=%s&type=%s" % (interObj.id,request.GET.get("option"),request.GET.get("type", "DATA_KEYWORD")))
   except:
       return render(request, "permission/page_404.html")

@single_page_permission
def operationCheck(request,context):
    langDict = getLangTextDict(request)
    context["id"] = request.GET.get("id",-1)
    context["option"] = request.GET.get("option")
    type = request.GET.get("type", "DATA_KEYWORD")
    if int(context["id"]) <= 0:
        key = request.GET.get("key")
        interObj = MainService.getDataByKey(key)
        return redirect("/datakeyword/operationCheck?id=%s&option=%s&type=%s" % (interObj.id,context["option"],type))

    context["datakeywordAdd"] = "current-page"

    if not isRelease:
        context["env"] = "test"
    try:
        context["dataAddBy"] = MainService.getDataById(request.GET.get("id")).addBy
    except Exception as e:
        return render(request, "permission/page_404.html")

    # 文本
    text = {}
    try:
        if request.GET.get("type", "DATA_KEYWORD") == "DATA_KEYWORD":
            context["title"] = "KEYWORD-" + request.GET.get("id")
            if context["option"]== "select":
                text["pageTitle"] = "查看数据关键字"
                text["subPageTitle"] = "数据关键字"
            elif context["option"] == "edit":
                text["pageTitle"] = "编辑数据关键字"
                text["subPageTitle"] = "数据关键字"
            elif context["option"] == "copy":
                text["pageTitle"] = "新增数据关键字"
                text["subPageTitle"] = "数据关键字"
        else:
            context["title"] = "PYTHON-" + request.GET.get("id")
            if context["option"] == "select":
                text["pageTitle"] = "查看PYTHON代码"
                text["subPageTitle"] = "PYTHON代码"
            elif context["option"] == "edit":
                text["pageTitle"] = "编辑PYTHON代码"
                text["subPageTitle"] = "PYTHON代码"
            elif context["option"] == "copy":
                text["pageTitle"] = "新增PYTHON代码"
                text["subPageTitle"] = "PYTHON代码"
    except Exception as e:
        return HttpResponse("参数错误 %s" % e)
    context["text"] = text
    context["importStr"] = getPythonThirdLib()
    return render(request, "data_keyword/add.html", context)

def getDataById(request):
    langDict = getLangTextDict(request)
    # 根据版本判断应该从哪个表里取数据 王吉亮添加于20180224
    getDBData = MainService.getDataByIdToDict(request.GET.get("id"))
    return HttpResponse(ApiReturn(ApiReturn.CODE_OK, langDict["web"]["httpInterfaceSuccess"], json.dumps(getDBData)).toJson())

@single_data_permission(Tb4DataKeyword,Tb4DataKeyword)
def saveEditData(request):
    postLoad = json.loads(request.POST.get("postData"))
    postLoad["modTime"] = datetime.datetime.now()
    postLoad["modBy"] = request.session.get("loginName")
    try:
        retCode,retV = MainService.dataSaveEdit(request,postLoad)
        addUserLog(request, "DataKeyword服务->更新[%s]->成功。" % id, "PASS")
        return HttpResponse(ApiReturn(code=retCode,message=str(retV)).toJson())
    except Exception as e:
        logger.error(traceback.format_exc())
        return HttpResponse(ApiReturn(ApiReturn.CODE_INTERFACE_ERROR, '保存编辑失败！%s' % e).toJson())

@single_data_permission(Tb4DataKeyword,Tb4DataKeyword)
def delData(request):
    id = request.GET.get("id")
    try:
        dataObj = MainService.getDataById(request.GET.get("id"))
        if dataObj.addBy != request.session.get("loginName"):
            return HttpResponse(ApiReturn(ApiReturn.CODE_INTERFACE_ERROR, "只能删除自己的用例").toJson())

    except Exception as e:
        print(traceback.format_exc())
        return HttpResponse(ApiReturn(ApiReturn.CODE_INTERFACE_ERROR, "参数id错误 %s" % e).toJson())

    if MainService.delDataById(request,id) == 1:
        addUserLog(request, "DataKeyword管理->删除[%s]->成功。" % id, "PASS")
        return HttpResponse(ApiReturn(ApiReturn.CODE_OK).toJson())
    else:
        return HttpResponse(ApiReturn(ApiReturn.CODE_INTERFACE_ERROR).toJson())



