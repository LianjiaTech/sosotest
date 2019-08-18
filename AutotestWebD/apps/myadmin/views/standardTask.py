from urllib import parse

# Create your views here.
from apps.common.config import commonWebConfig
from apps.common.func.WebFunc import *
from apps.myadmin.service.StandardTaskService import StandardTaskService

logger = logging.getLogger("django")

def standardTaskCheckPage(request):
    context = {}
    context["standardTask_check"] = "active"
    return render(request, "myadmin/standardTask/admin_standardTask_check.html", context)

def getStandardTask(request):
    checkArr = json.loads(parse.unquote(request.POST.get("checkArr")))
    orderBy = request.POST.get("orderBy", "")
    page = request.POST.get("page")

    if isInt(page):
        page = int(page)
    else:
        addUserLog(request, "单接口管理->查看用例->获取数据->页面参数不合法", "FAIL")
        return HttpResponse("<script>alert('请验证页数参数');</script>")
    execSql = "SELECT u.* from tb_webPortal_standard_task u WHERE 1=1 "
    checkList = []
    for key in checkArr:
        if checkArr[key] == "":
            continue
        checkList.append("%%%s%%" % checkArr[key])
        execSql += """ and u.%s """ % key
        execSql += """ LIKE %s"""
    execSql += """ ORDER BY %s""" % orderBy
    context = pagination(sqlStr=execSql,attrList=checkList,page=page,pageNum=commonWebConfig.userPageNum)
    response = render(request, "myadmin/standardTask/subPages/standardTask_sub_page.html",context)
    return response


def getStandardTaskForId(request):
    standardTaskId = request.POST.get("standardTaskId")
    try:
        standardTaskData = TbWebPortalStandardTask.objects.get(id=standardTaskId)
    except Exception as e:
        message = "标准任务版本查询出错 %s" % e
        logger.error(message)
        return HttpResponse(ApiReturn(code=ApiReturn.CODE_WARNING, message=message).toJson())
    return HttpResponse(ApiReturn(body=dbModelToDict(standardTaskData)).toJson())

def getAllVersions(request):
    versionsList = []
    versions = TbVersion.objects.filter(state=1)
    if len(versions) != 0:
        for version in versions:
            versionsList.append(version.versionName)
    return HttpResponse(ApiReturn(body=versionsList).toJson())

def copyTaskToOtherVersion(request):
    standardTaskData = json.loads(request.POST.get("standardTaskData"))
    goalVersion = standardTaskData["goalVersion"]
    nowVersion = standardTaskData["nowVersion"]
    if goalVersion == nowVersion:
        print("333333333333")
        return HttpResponse(ApiReturn(code=ApiReturn.CODE_WARNING, message="历史版本和目标版本不能一样").toJson())
    standardTasks = TbWebPortalStandardTask.objects.filter(state=1, version=nowVersion)
    for standardTask in standardTasks:
        standardTaskObject = TbWebPortalStandardTask()
        standardTaskObject.version = goalVersion
        standardTaskObject.businessLine = standardTask.businessLine
        standardTaskObject.team = standardTask.team
        standardTaskObject.head = standardTask.head
        standardTaskObject.taskId = standardTask.taskId
        standardTaskObject.state = 1
        standardTaskObject.save()
    return HttpResponse(ApiReturn().toJson())


def addStandardTask(request):
    standardTaskData = json.loads(request.POST.get("standardTaskData"))
    logger.info("addPermission %s" % request.POST.get("permissionData"))
    version = standardTaskData["version"]
    businessLine = standardTaskData["businessLine"]
    team = standardTaskData["team"]
    head = standardTaskData["head"]
    taskId = standardTaskData["taskId"]
    searchResult = dbModelListToListDict(TbWebPortalStandardTask.objects.filter(version=version, businessLine=businessLine, team=team, head=head, taskId=taskId))
    if len(searchResult) == 0:
        result = TbWebPortalStandardTask()
        result.version = version
        result.businessLine = businessLine
        result.team = team
        result.head = head
        result.taskId = taskId
        result.save()
        if result:
            logger.info("addStandardTask 标准数据版本创建成功 %s" % result)
        return HttpResponse(ApiReturn().toJson())
    else:

        searchResultDict = searchResult[0]
        if searchResultDict["state"] == 0:
            searchResultDict["state"] = 1
            searchResultDict["version"] = version
            searchResultDict["businessLine"] = businessLine
            searchResultDict["team"] = team
            searchResultDict["head"] = head
            searchResultDict["taskId"] = taskId
            StandardTaskService.updatePermission(searchResultDict)
            return HttpResponse(ApiReturn().toJson())
        else:
            logger.info("addStandardTask 标准数据版本创建失败")
            return HttpResponse(
                ApiReturn(code=ApiReturn.CODE_WARNING, message="标准数据版本创建失败,请检查数据是否重复").toJson())

    return HttpResponse(ApiReturn().toJson())


def editStandardTask(request):
    try:
        standardTaskData =json.loads(request.POST.get("standardTaskData"))
        StandardTaskService.updatePermission(standardTaskData)
    except Exception as e:
        print(traceback.format_exc())
        message = "编辑标准数据版本发生异常 %s" % e
        logger.info(message)
        return HttpResponse(ApiReturn(code=ApiReturn.CODE_WARNING, message=message).toJson())
    return HttpResponse(ApiReturn().toJson())

def delStandardTask(request):
    standardTaskId = request.POST.get("standardTaskId", "")
    if not standardTaskId:
        return HttpResponse(ApiReturn(ApiReturn.CODE_WARNING, message="standardTaskId参数错误").toJson())
    try:
        standardTaskData = TbWebPortalStandardTask.objects.get(state=1, id=standardTaskId)
    except Exception as e:
        return HttpResponse(ApiReturn(ApiReturn.CODE_WARNING, message="standardTaskId查询错误 %s" % e).toJson())
    standardTaskData.state = 0
    standardTaskData.save()
    return HttpResponse(ApiReturn().toJson())

def resetStandardTask(request):
    standardTaskId = request.POST.get("standardTaskId", "")
    if not standardTaskId:
        return HttpResponse(ApiReturn(ApiReturn.CODE_WARNING, message="standardTaskId参数错误").toJson())
    try:
        standardTaskData = TbWebPortalStandardTask.objects.get(state=0, id=standardTaskId)
    except Exception as e:
        return HttpResponse(ApiReturn(ApiReturn.CODE_WARNING, message="standardTaskId查询错误 %s" % e).toJson())
    standardTaskData.state = 1
    standardTaskData.save()

    return HttpResponse(ApiReturn().toJson())

