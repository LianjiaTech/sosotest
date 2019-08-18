
from urllib import parse

from apps.common.config import commonWebConfig
from apps.common.func.LanguageFunc import *
from apps.common.func.WebFunc import addUserLog
from apps.common.model.RedisDBConfig import *
from apps.config.services.businessLineService import *
from apps.config.services.modulesService import *
from apps.statistic_task.services.main_service import MainService

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
    context["statisticTaskCheck"] = "current-page"
    context["userName"] = request.session.get("userName")
    context["checkBusinessLine"] = dbModelListToListDict(BusinessService.getAllBusinessLine())
    context["checkModules"] = dbModelListToListDict(ModulesService.getAllModules())
    # 文本
    text = {}
    text["pageTitle"] = "统计任务"
    context["text"] = text
    context["page"] = 1
    # context["lang"] = getLangTextDict(request)
    addUserLog(request, "StatisticTask管理->查看->页面展示->成功", "PASS")
    return render(request, "statistic_task/list.html", context)

def listData(request):
    page = request.POST.get("page")
    if isInt(page):
        page = int(page)
    else:
        addUserLog(request, "StatisticTask管理->查看用例->获取数据->页面参数不合法", "FAIL")
        return HttpResponse("<script>alert('请验证页数参数');</script>")
    checkArr = json.loads(parse.unquote(request.POST.get("checkArr")))

    orderBy = request.POST.get("orderBy")
    if isSqlInjectable(orderBy):
        addUserLog(request, "StatisticTask管理->查看用例->获取数据->SQL注入检测时发现查询条件非法", "FAIL")
        return HttpResponse("<script>alert('查询条件非法');</script>")

    tbName = "tb4_statistic_task"
    versionCondition = ""

    execSql = "SELECT i.*,u.userName,mu.userName modByName,m.moduleName moduleName,b.bussinessLineName businessLineName from %s i LEFT JOIN tb_user mu ON i.modBy = mu.loginName LEFT JOIN tb_user u ON i.addBy = u.loginName LEFT JOIN  tb_modules m ON i.moduleId = m.id LEFT JOIN tb_business_line b ON i.businessLineId = b.id   WHERE 1=1 and i.state=1 %s" % (
    tbName, versionCondition)
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
    context = pagination(sqlStr=execSql, attrList=checkList, page=page, pageNum=commonWebConfig.interFacePageNum)
    for index in context["pageDatas"]:
        if index["addBy"] not in otherUserList:
            otherUserList.append(index["addBy"])

    response = render(request, "statistic_task/SubPages/list_data.html", context)
    addUserLog(request, "StatisticTask管理->查看->获取数据->成功", "PASS")
    return response

def addPage(request):
    context = {}
    context["option"] = "add"
    context["addStatisticTask"] = "current-page"
    if not isRelease:
        context["env"] = "test"
    # 文本
    text = {}
    text["pageTitle"] = "添加统计任务"
    text["subPageTitle"] = "添加统计任务"
    context["text"] = text

    context["businessLine"] = dbModelListToListDict(BusinessService.getAllBusinessLine()) #初始化业务线

    permission = []
    permission.append("HTTP_interface_add") #加数据为了测试
    permission.append("HTTP_interface_edit")
    permission.append("HTTP_interface_copy")
    context["permission"] = permission
    addUserLog(request, "StatisticTask管理->添加->页面展示->成功", "PASS")
    return render(request, "statistic_task/add.html", context)

def addData(request):
    # 当前版本使用历史代码，不更新。
    if request.method != 'POST':
        return HttpResponse(ApiReturn(ApiReturn.CODE_METHOD_ERROR, "请求方式错误", "").toJson())
    print(request.POST)
    data = json.loads(request.POST.get("postData"))
    try:
        retCode,retValue = MainService.addData(data, request.session.get("loginName"))
        return HttpResponse(ApiReturn(retCode, retValue, "").toJson())
    except Exception as e:
        logger.error(traceback.format_exc())
        return HttpResponse(ApiReturn(ApiReturn.CODE_INTERFACE_ERROR, "添加StatisticTask错误", "Failed: %s" % e).toJson())

def operationCheck(request):
    langDict = getLangTextDict(request)
    context = {}
    context["id"] = request.GET.get("id")
    context["option"] = request.GET.get("option")
    context["addStatisticTask"] = "current-page"
    context["businessLine"] = dbModelListToListDict(BusinessService.getAllBusinessLine()) #初始化业务线

    if not isRelease:
        context["env"] = "test"
    try:
        context["dataAddBy"] = MainService.getDataById(request.GET.get("id")).addBy
    except Exception as e:
        return render(request, "permission/page_404.html")

    # 文本
    text = {}
    try:
        if context["option"]== "select":
            text["pageTitle"] = "查看统计任务"
            text["subPageTitle"] = "统计任务"
        elif context["option"] == "edit":
            text["pageTitle"] = "编辑统计任务"
            text["subPageTitle"] = "统计任务"
        elif context["option"] == "copy":
            text["pageTitle"] = "新增统计任务"
            text["subPageTitle"] = "统计任务"
    except Exception as e:
        return HttpResponse("参数错误 %s" % e)
    context["text"] = text
    return render(request, "statistic_task/add.html", context)

def getDataById(request):
    langDict = getLangTextDict(request)
    # 根据版本判断应该从哪个表里取数据 王吉亮添加于20180224
    getDBData = MainService.getDataByIdToDict(request.GET.get("id"))
    return HttpResponse(ApiReturn(ApiReturn.CODE_OK, langDict["web"]["httpInterfaceSuccess"], json.dumps(getDBData)).toJson())

def saveEditData(request):
    postLoad = json.loads(request.POST.get("postData"))
    postLoad["modTime"] = datetime.datetime.now()
    postLoad["modBy"] = request.session.get("loginName")
    try:
        retCode,retV = MainService.dataSaveEdit(request,postLoad)
        addUserLog(request, "StatisticTask服务->更新[%s]->成功。" % id, "PASS")
        return HttpResponse(ApiReturn(code=retCode,message=str(retV)).toJson())
    except Exception as e:
        logger.error(traceback.format_exc())
        return HttpResponse(ApiReturn(ApiReturn.CODE_INTERFACE_ERROR, '保存编辑失败！%s' % e).toJson())

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
        addUserLog(request, "StatisticTask管理->删除[%s]->成功。" % id, "PASS")
        return HttpResponse(ApiReturn(ApiReturn.CODE_OK).toJson())
    else:
        return HttpResponse(ApiReturn(ApiReturn.CODE_INTERFACE_ERROR).toJson())


def executeListPage(request):
    request.session['groupLevel1'] = groupLevel1
    request.session['groupLevel2'] = groupLevel2
    request.session['isReleaseEnv'] = isRelease

    langDict = getLangTextDict(request)
    context = {}
    if not isRelease:
        context["env"] = "test"
    context["execStatisticTaskCheck"] = "current-page"
    context["userName"] = request.session.get("userName")
    context["checkBusinessLine"] = dbModelListToListDict(BusinessService.getAllBusinessLine())
    context["checkModules"] = dbModelListToListDict(ModulesService.getAllModules())
    # 文本
    text = {}
    text["pageTitle"] = "统计任务上报结果"
    context["text"] = text
    context["page"] = 1
    # context["lang"] = getLangTextDict(request)
    addUserLog(request, "StatisticTask管理->查看->页面展示->成功", "PASS")
    return render(request, "statistic_task/exec_list.html", context)

def executeListData(request):
    page = request.POST.get("page")
    if isInt(page):
        page = int(page)
    else:
        addUserLog(request, "StatisticTask管理->查看用例->获取数据->页面参数不合法", "FAIL")
        return HttpResponse("<script>alert('请验证页数参数');</script>")
    checkArr = json.loads(parse.unquote(request.POST.get("checkArr")))

    orderBy = request.POST.get("orderBy")
    if isSqlInjectable(orderBy):
        addUserLog(request, "StatisticTask管理->查看用例->获取数据->SQL注入检测时发现查询条件非法", "FAIL")
        return HttpResponse("<script>alert('查询条件非法');</script>")

    tbName = "tb4_statistic_task_execute_info"
    versionCondition = ""

    execSql = "SELECT i.*,u.userName,mu.userName modByName,m.moduleName moduleName,b.bussinessLineName businessLineName from %s i LEFT JOIN tb_user mu ON i.modBy = mu.loginName LEFT JOIN tb_user u ON i.addBy = u.loginName LEFT JOIN  tb_modules m ON i.moduleId = m.id LEFT JOIN tb_business_line b ON i.businessLineId = b.id   WHERE 1=1 and i.state=1 %s" % (
    tbName, versionCondition)
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
        elif key == "statisticTaskId":
            checkList.append("%s" % checkArr[key])
            execSql += """ and i.statisticTaskId = %s """
            continue
        elif key == "testResult":
            checkList.append("%s" % checkArr[key])
            execSql += """ and i.testResult = %s """
            continue
        checkList.append("%%%s%%" % checkArr[key])
        execSql += """ and i.%s """ % key
        execSql += """ LIKE %s"""
    execSql += """ ORDER BY %s""" % orderBy
    otherUserList = []
    context = pagination(sqlStr=execSql, attrList=checkList, page=page, pageNum=commonWebConfig.interFacePageNum)
    for index in context["pageDatas"]:
        if index["addBy"] not in otherUserList:
            otherUserList.append(index["addBy"])
        index["executeDetailTextDict"] = json.loads(index['executeDetailText'])

    response = render(request, "statistic_task/SubPages/exec_list_data.html", context)
    addUserLog(request, "StatisticTask管理->查看->获取数据->成功", "PASS")
    return response

def operationExecCheck(request):
    langDict = getLangTextDict(request)
    context = {}
    context["id"] = request.GET.get("id")
    context["option"] = request.GET.get("option")
    context["addStatisticTask"] = "current-page"
    context["businessLine"] = dbModelListToListDict(BusinessService.getAllBusinessLine()) #初始化业务线

    if not isRelease:
        context["env"] = "test"
    try:
        context["dataAddBy"] = MainService.getDataById(request.GET.get("id")).addBy
    except Exception as e:
        return render(request, "permission/page_404.html")

    # 文本
    text = {}
    try:
        if context["option"]== "select":
            text["pageTitle"] = "查看统计任务"
            text["subPageTitle"] = "统计任务"
        elif context["option"] == "edit":
            text["pageTitle"] = "编辑统计任务"
            text["subPageTitle"] = "统计任务"
        elif context["option"] == "copy":
            text["pageTitle"] = "新增统计任务"
            text["subPageTitle"] = "统计任务"
    except Exception as e:
        return HttpResponse("参数错误 %s" % e)
    context["text"] = text
    return render(request, "statistic_task/add.html", context)

def setReason(request):
    id = request.GET.get("id")
    reason = request.GET.get("reason")
    try:
        retCode,retInfo = MainService.dataSaveEditSetReason(id,reason)
        if retCode == 10000:
            addUserLog(request, "StatisticTask管理->删除[%s]->成功。" % id, "PASS")
            return HttpResponse(ApiReturn(ApiReturn.CODE_OK).toJson())
        else:
            return HttpResponse(ApiReturn(code=retCode,message=retmsg).toJson())
    except Exception as e:
        print(traceback.format_exc())
        return HttpResponse(ApiReturn(ApiReturn.CODE_INTERFACE_ERROR, "参数id错误 %s" % e).toJson())

