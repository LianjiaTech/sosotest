from urllib import parse

# Create your views here.
from apps.common.config import commonWebConfig
from apps.common.func.WebFunc import *
from apps.myadmin.service.StandardEnvService import StandardEnvService

logger = logging.getLogger("django")

def standardEnvCheckPage(request):
    context = {}
    context["standardEnv_check"] = "active"
    return render(request, "myadmin/standardEnv/admin_standardEnv_check.html", context)

def getStandardEnv(request):
    checkArr = json.loads(parse.unquote(request.POST.get("checkArr")))
    orderBy = request.POST.get("orderBy", "")
    page = request.POST.get("page")

    if isInt(page):
        page = int(page)
    else:
        addUserLog(request, "单接口管理->查看用例->获取数据->页面参数不合法", "FAIL")
        return HttpResponse("<script>alert('请验证页数参数');</script>")
    execSql = "SELECT u.* from tb_webPortal_standard_Env u WHERE 1=1 "
    checkList = []
    for key in checkArr:
        if checkArr[key] == "":
            continue
        checkList.append("%%%s%%" % checkArr[key])
        execSql += """ and u.%s """ % key
        execSql += """ LIKE %s"""
    execSql += """ ORDER BY %s""" % orderBy
    context = pagination(sqlStr=execSql,attrList=checkList,page=page,pageNum=commonWebConfig.userPageNum)
    response = render(request, "myadmin/standardEnv/subPages/standardEnv_sub_page.html", context)
    return response


def getStandardEnvForId(request):
    standardEnvId = request.POST.get("standardEnvId")
    try:
        standardEnvData = TbWebPortalStandardEnv.objects.get(id=standardEnvId)
    except Exception as e:
        message = "standardEnv查询出错 %s" % e
        logger.error(message)
        return HttpResponse(ApiReturn(code=ApiReturn.CODE_WARNING, message=message).toJson())
    return HttpResponse(ApiReturn(body=dbModelToDict(standardEnvData)).toJson())


def addStandardEnv(request):
    standardEnvData = json.loads(request.POST.get("standardEnvData"))
    logger.info("standardEnvData %s" % request.POST.get("standardEnvData"))
    httpConfKey = standardEnvData["httpConfKey"]
    openApiKey = standardEnvData["openApiKey"]
    rmiKey = standardEnvData["rmiKey"]
    version = standardEnvData["version"]
    actionIsShow = standardEnvData["actionIsShow"]
    rmiIsShow = standardEnvData["rmiIsShow"]
    openapiIsShow = standardEnvData["openapiIsShow"]
    uiIsShow = standardEnvData["uiIsShow"]
    alias = standardEnvData["alias"]
    lineSort = standardEnvData["lineSort"]

    searchResult = dbModelListToListDict(TbWebPortalStandardEnv.objects.filter(httpConfKey=httpConfKey))
    if len(searchResult) == 0:
        result = TbWebPortalStandardEnv()
        result.httpConfKey = httpConfKey
        result.openApiKey = openApiKey
        result.rmiKey = rmiKey
        result.version = version
        result.alias = alias
        result.actionIsShow = actionIsShow
        result.rmiIsShow = rmiIsShow
        result.openapiIsShow = openapiIsShow
        result.uiIsShow = uiIsShow
        result.lineSort = lineSort
        result.save()
        if result:
            logger.info("addStandardEnv standardEnv创建成功 %s" % result)
        return HttpResponse(ApiReturn().toJson())
    else:
        searchResultDict = searchResult[0]
        if searchResultDict["state"] == 0:
            searchResultDict["state"] = 1
            searchResultDict["httpConfKey"] = httpConfKey
            searchResultDict["openApiKey"] = openApiKey
            searchResultDict["rmiKey"] = rmiKey
            searchResultDict["version"] = version
            searchResultDict["alias"] = alias
            searchResultDict["actionIsShow"] = actionIsShow
            searchResultDict["rmiIsShow"] = rmiIsShow
            searchResultDict["openapiIsShow"] = openapiIsShow
            searchResultDict["uiIsShow"] = uiIsShow
            searchResultDict["lineSort"] = lineSort
            StandardEnvService.updateStandardEnvService(searchResultDict)
            return HttpResponse(ApiReturn().toJson())
        else:
            logger.info("addStandardEnv standardEnv创建失败")
            return HttpResponse(
                ApiReturn(code=ApiReturn.CODE_WARNING, message="standardEnv创建失败,请检查数据是否重复").toJson())

    return HttpResponse(ApiReturn().toJson())


def editStandardEnv(request):
    try:
        standardEnvData =json.loads(request.POST.get("standardEnvData"))
        StandardEnvService.updateStandardEnvService(standardEnvData)
    except Exception as e:
        print(traceback.format_exc())
        message = "编辑standardEnv发生异常 %s" % e
        logger.info(message)
        return HttpResponse(ApiReturn(code=ApiReturn.CODE_WARNING, message=message).toJson())
    return HttpResponse(ApiReturn().toJson())

def deleteStandardEnv(request):
    standardEnvId = request.POST.get("standardEnvId", "")
    if not standardEnvId:
        return HttpResponse(ApiReturn(ApiReturn.CODE_WARNING, message="standardEnvId参数错误").toJson())
    try:
        standardEnvData = TbWebPortalStandardEnv.objects.get(state=1, id=standardEnvId)
    except Exception as e:
        return HttpResponse(ApiReturn(ApiReturn.CODE_WARNING, message="standardEnvId查询错误 %s" % e).toJson())
    standardEnvData.state = 0
    standardEnvData.save()
    return HttpResponse(ApiReturn().toJson())

def resetStandardEnv(request):
    standardEnvId = request.POST.get("standardEnvId", "")
    if not standardEnvId:
        return HttpResponse(ApiReturn(ApiReturn.CODE_WARNING, message="standardEnvId参数错误").toJson())
    try:
        standardEnvData = TbWebPortalStandardEnv.objects.get(state=0, id=standardEnvId)
    except Exception as e:
        return HttpResponse(ApiReturn(ApiReturn.CODE_WARNING, message="standardEnvId查询错误 %s" % e).toJson())
    standardEnvData.state = 1
    standardEnvData.save()

    return HttpResponse(ApiReturn().toJson())

