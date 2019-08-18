from urllib import parse

# Create your views here.
from apps.common.config import commonWebConfig
from apps.common.func.WebFunc import *
from apps.myadmin.service.UiMobileServer import UiMobileServer

logger = logging.getLogger("django")

def uiMobileServerCheckPage(request):
    context = {}
    context["uiMobileServer_check"] = "active"
    return render(request, "myadmin/uiMobileServer/admin_uiMobileServer_check.html", context)

def getUiMobileServer(request):
    checkArr = json.loads(parse.unquote(request.POST.get("checkArr")))
    orderBy = request.POST.get("orderBy","")
    page = request.POST.get("page")
    if isInt(page):
        page = int(page)
    else:
        return HttpResponse("<script>alert('请验证页数参数');</script>")
    execSql = "SELECT u.* from tb_ui_mobile_server u WHERE 1=1  "
    checkList = []
    for key in checkArr:
        if checkArr[key] == "":
            continue
        checkList.append("%%%s%%" % checkArr[key])
        execSql += """ and u.%s """ % key
        execSql += """ LIKE %s"""
    execSql += """ ORDER BY %s""" % orderBy
    context = pagination(sqlStr=execSql, attrList=checkList, page=page, pageNum=commonWebConfig.userPageNum)
    response = render(request, "myadmin/uiMobileServer/subPages/uiMobileServer_sub_page.html", context)
    return response

def addUiMobileServer(request):
    uiMobileServerData = json.loads(request.POST.get("uiMobileServerData"))
    serverName = uiMobileServerData["serverName"]
    serverDesc = uiMobileServerData["serverDesc"]
    serverType = uiMobileServerData["serverType"]
    status = uiMobileServerData["status"]
    executeTaskId = uiMobileServerData["executeTaskId"]
    serverIp = uiMobileServerData["serverIp"]
    serverPort = uiMobileServerData["serverPort"]
    udid = uiMobileServerData["udid"]
    deviceName = uiMobileServerData["deviceName"]
    wdaLocalPort = uiMobileServerData["wdaLocalPort"]

    searchResult = dbModelListToListDict(TbUiMobileServer.objects.filter(serverName=serverName))
    if len(searchResult) == 0:
        result = TbUiMobileServer()
        result.serverName = serverName
        result.serverDesc = serverDesc
        result.serverType = serverType
        result.status = status
        result.executeTaskId = executeTaskId
        result.serverIp = serverIp
        result.serverPort = serverPort
        result.udid = udid
        result.deviceName = deviceName
        result.wdaLocalPort = wdaLocalPort
        result.save()
        if result:
            logger.info("addUiMobileServer uiMobileServer创建成功 %s" % result)
        return HttpResponse(ApiReturn().toJson())
    else:
        searchResultDict = searchResult[0]
        if searchResultDict["state"] == 0:
            searchResultDict["state"] = 1
            searchResultDict["serverName"] = serverName
            searchResultDict["serverDesc"] = serverDesc
            searchResultDict["serverType"] = serverType
            searchResultDict["status"] = status
            searchResultDict["executeTaskId"] = executeTaskId
            searchResultDict["serverIp"] = serverIp
            searchResultDict["serverPort"] = serverPort
            searchResultDict["udid"] = udid
            searchResultDict["deviceName"] = deviceName
            searchResultDict["wdaLocalPort"] = wdaLocalPort
            UiMobileServer.updateUiMobileServer(searchResultDict)
            return HttpResponse(ApiReturn().toJson())
        else:
            logger.info("addUiMobileServer uiMobileServer创建失败")
            return HttpResponse(ApiReturn(code=ApiReturn.CODE_WARNING, message="uiMobileServer创建失败,请检查数据是否重复").toJson())

    return HttpResponse(ApiReturn().toJson())


def getUiMobileServerForId(request):
    uiMobileServerId = request.POST.get("uiMobileServerId")
    try:
        uiMobileServerData = TbUiMobileServer.objects.get(id=uiMobileServerId)
    except Exception as e:
        message = "uiMobileServer查询出错 %s" % e
        logger.error(message)
        return HttpResponse(ApiReturn(code=ApiReturn.CODE_WARNING, message=message).toJson())
    return HttpResponse(ApiReturn(body=dbModelToDict(uiMobileServerData)).toJson())


def editUiMobileServer(request):
    try:
        uiMobileServerData =json.loads(request.POST.get("uiMobileServerData"))
        UiMobileServer.updateUiMobileServer(uiMobileServerData)
    except Exception as e:
        print(traceback.format_exc())
        message = "编辑uiMobileServer发生异常 %s" % e
        logger.info(message)
        return HttpResponse(ApiReturn(code=ApiReturn.CODE_WARNING, message=message).toJson())
    return HttpResponse(ApiReturn().toJson())

def deleteUiMobileServer(request):
    uiMobileServerId = request.POST.get("uiMobileServerId", "")
    if not uiMobileServerId:
        return HttpResponse(ApiReturn(ApiReturn.CODE_WARNING, message="uiMobileServerId参数错误").toJson())
    try:
        uiMobileServerData = TbUiMobileServer.objects.get(state=1, id=uiMobileServerId)
    except Exception as e:
        return HttpResponse(ApiReturn(ApiReturn.CODE_WARNING, message="uiMobileServerId查询错误 %s" % e).toJson())
    uiMobileServerData.state = 0
    uiMobileServerData.save()
    return HttpResponse(ApiReturn().toJson())

def resetUiMobileServer(request):
    uiMobileServerId = request.POST.get("uiMobileServerId", "")
    if not uiMobileServerId:
        return HttpResponse(ApiReturn(ApiReturn.CODE_WARNING, message="uiMobileServerId参数错误").toJson())
    try:
        uiMobileServerData = TbUiMobileServer.objects.get(state=0, id=uiMobileServerId)
    except Exception as e:
        return HttpResponse(ApiReturn(ApiReturn.CODE_WARNING, message="uiMobileServerId查询错误 %s" % e).toJson())
    uiMobileServerData.state = 1
    uiMobileServerData.save()

    return HttpResponse(ApiReturn().toJson())
