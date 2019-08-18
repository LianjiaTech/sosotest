from urllib import parse

# Create your views here.
from all_models.models import *
from apps.common.config import commonWebConfig
from apps.common.func.WebFunc import *
from apps.myadmin.service.ConfigHttpService import ConfigHttpService
from apps.myadmin.service.HttpInterfaceDebugService import HttpInterfaceDebugService

logger = logging.getLogger("django")

def httpInterfaceDebugCheckPage(request):
    context = {}
    context["httpInterfaceDebug_check"] = "active"
    return render(request, "myadmin/httpInterfaceDebug/admin_httpInterfaceDebug_check.html",context)

def getHttpInterfaceDebug(request):
    checkArr = json.loads(parse.unquote(request.POST.get("checkArr")))

    orderBy = request.POST.get("orderBy","")
    page = request.POST.get("page")
    if isInt(page):
        page = int(page)
    else:
        addUserLog(request, "单接口管理->查看用例->获取数据->页面参数不合法", "FAIL")
        return HttpResponse("<script>alert('请验证页数参数');</script>")
    execSql = "SELECT u.* from tb_http_interface_debug u WHERE 1=1 "
    checkList = []
    for key in checkArr:
        if checkArr[key] == "":
            continue
        checkList.append("%%%s%%" % checkArr[key])
        execSql += """ and u.%s """ % key
        execSql += """ LIKE %s"""
    execSql += """ ORDER BY %s""" % orderBy
    context = pagination(sqlStr=execSql, attrList=checkList, page=page, pageNum=commonWebConfig.userPageNum)
    response = render(request, "myadmin/httpInterfaceDebug/subPages/httpInterfaceDebug_sub_page.html", context)
    return response

def getHttpInterfaceDebugForId(request):
    httpInterfaceDebugId = request.POST.get("httpInterfaceDebugId")
    try:
        httpInterfaceDebugData = TbHttpInterfaceDebug.objects.get(id=httpInterfaceDebugId)
        requestDict = dbModelToDict(httpInterfaceDebugData)
        del requestDict["businessLineId_id"]
        requestDict["businessLineId"] = httpInterfaceDebugData.businessLineId.bussinessLineName
        del requestDict["moduleId_id"]
        requestDict["moduleId"] = httpInterfaceDebugData.moduleId.moduleName
        del requestDict["sourceId_id"]
        requestDict["sourceId"] = httpInterfaceDebugData.sourceId.sourceName
        del requestDict["httpConfKey_id"]
        requestDict["httpConfKey"] = httpInterfaceDebugData.httpConfKey.httpConfKey
        del requestDict["addBy_id"]
        requestDict["addBy"] = httpInterfaceDebugData.addBy.userName + "(" + httpInterfaceDebugData.addBy.loginName + ")"

    except Exception as e:
        message = "查询环境配置出错 %s" % e
        logger.error(message)
        return HttpResponse(ApiReturn(code=ApiReturn.CODE_WARNING, message=message).toJson())
    return HttpResponse(ApiReturn(body=requestDict).toJson())

def getAllBusinessLines(request):
    businessLines = TbBusinessLine.objects.filter(state=1)
    bussinessLineNamesList = []
    if len(businessLines) == 0:
        return HttpResponse(ApiReturn(code=ApiReturn.CODE_WARNING,message="没有可有的业务线，请联系管理员"))
    for businessLine in businessLines:
        if businessLine.bussinessLineName not in bussinessLineNamesList:
            bussinessLineNamesList.append(businessLine.bussinessLineName)
    return HttpResponse(ApiReturn(body=bussinessLineNamesList).toJson())

def getAllModuleNames(request):
    modules = TbModules.objects.filter(state=1)
    moduleNamesList = []
    if len(modules) == 0:
        return HttpResponse(ApiReturn(code=ApiReturn.CODE_WARNING,message="没有可有的模块，请联系管理员"))
    for module in modules:
        if module.moduleName not in modules:
            moduleNamesList.append(module.moduleName)
    return HttpResponse(ApiReturn(body=moduleNamesList).toJson())

def getAllSourceNames(request):
    sources = TbSource.objects.filter(state=1)
    sourceNamesList = []
    if len(sources) == 0:
        return HttpResponse(ApiReturn(code=ApiReturn.CODE_WARNING,message="没有可有的来源，请联系管理员"))
    for source in sources:
        if source.sourceName not in sources:
            sourceNamesList.append(source.sourceName)
    return HttpResponse(ApiReturn(body=sourceNamesList).toJson())

def getAllHttpConfKeys(request):
    configHttps = TbConfigHttp.objects.filter(state=1)
    if len(configHttps) == 0:
        return HttpResponse(ApiReturn(code=ApiReturn.CODE_WARNING, message="没有可用的环境配置，请联系管理员"))
    httpConfKeyslist = []
    for configHttp in configHttps:
        if configHttp.httpConfKey not in httpConfKeyslist:
            httpConfKeyslist.append(configHttp.httpConfKey)
    return HttpResponse(ApiReturn(body=httpConfKeyslist).toJson())

def getAllUsers(request):
    users = TbUser.objects.filter(state=1)
    if len(users) == 0:
        return HttpResponse(ApiReturn(code=ApiReturn.CODE_WARNING, message="没有可用的用户，请联系管理员"))
    usersList = []
    for user in users:
        if user.userName not in usersList:
            usersList.append(user.userName+"(" +user.loginName+")")
    return HttpResponse(ApiReturn(body=usersList).toJson())

def addHttpInterfaceDebug(request):
    httpInterfaceDebugData = json.loads(request.POST.get("httpInterfaceDebugData"))
    logger.info("addHttpInterfaceDebug %s" % request.POST.get("httpInterfaceDebugData"))
    searchResult = TbHttpInterfaceDebug.objects.filter(interfaceId=httpInterfaceDebugData["interfaceId"])
    try:
        if len(searchResult) == 0:
            result = TbHttpInterfaceDebug()
            result.interfaceId = httpInterfaceDebugData["interfaceId"]
            result.title = httpInterfaceDebugData["title"]
            result.casedesc = httpInterfaceDebugData["casedesc"]
            result.businessLineId = TbBusinessLine.objects.get(bussinessLineName=httpInterfaceDebugData["businessLineId"], state=1)
            result.moduleId = TbModules.objects.get(moduleName=httpInterfaceDebugData["moduleId"], state=1)
            result.sourceId = TbSource.objects.get(sourceName=httpInterfaceDebugData["sourceId"], state=1)
            result.caselevel = httpInterfaceDebugData["caselevel"]
            result.status = httpInterfaceDebugData["status"]
            result.caseType = httpInterfaceDebugData["caseType"]
            result.varsPre = httpInterfaceDebugData["varsPre"]
            result.uri = httpInterfaceDebugData["uri"]
            result.method = httpInterfaceDebugData["method"]
            result.header = httpInterfaceDebugData["header"]
            result.url = httpInterfaceDebugData["url"]
            result.params = httpInterfaceDebugData["params"]
            result.bodyType = httpInterfaceDebugData["bodyType"]
            result.bodyContent = httpInterfaceDebugData["bodyContent"]
            result.timeout = httpInterfaceDebugData["timeout"]
            result.varsPost = httpInterfaceDebugData["varsPost"]
            result.performanceTime = httpInterfaceDebugData["performanceTime"]
            result.execStatus = httpInterfaceDebugData["execStatus"]
            result.httpConfKey = TbConfigHttp.objects.get(httpConfKey=httpInterfaceDebugData["httpConfKey"], state=1)
            result.actualResult = httpInterfaceDebugData["actualResult"]
            result.assertResult = httpInterfaceDebugData["assertResult"]
            result.testResult = httpInterfaceDebugData["testResult"]
            result.beforeExecuteTakeTime = httpInterfaceDebugData["beforeExecuteTakeTime"]
            result.afterExecuteTakeTime = httpInterfaceDebugData["afterExecuteTakeTime"]
            result.executeTakeTime = httpInterfaceDebugData["executeTakeTime"]
            result.totalTakeTime = httpInterfaceDebugData["totalTakeTime"]
            result.version = httpInterfaceDebugData["version"]
            result.addBy = TbUser.objects.get(loginName=httpInterfaceDebugData["addBy"].split("(")[1].split(")")[0], state=1)
            result.save()
            if result:
                logger.info("addHttpInterfaceDebug 接口调试添加成功 %s" % result)
            return HttpResponse(ApiReturn().toJson())
        else:
            if searchResult.state == 0:
                searchResult.state = 1
                searchResult.save()
                return HttpResponse(ApiReturn().toJson())
            else:
                logger.info("addHttpInterfaceDebug 接口调试添加失败")
                return HttpResponse(ApiReturn(code=ApiReturn.CODE_WARNING, message="接口调试添加失败,请检查账号是否重复").toJson())
    except Exception as e:
        message = "接口调试添加失败 :%s" % e
        logger.info(message)
        return HttpResponse(ApiReturn(code=ApiReturn.CODE_WARNING, message="接口调试添加失败,请检查账号是否重复").toJson())


def editHttpInterfaceDebug(request):
    try:
        httpInterfaceDebugData = json.loads(request.POST.get("httpInterfaceDebugData"))
        result = TbHttpInterfaceDebug.objects.get(id=httpInterfaceDebugData["id"])
        result.interfaceId = httpInterfaceDebugData["interfaceId"]
        result.title = httpInterfaceDebugData["title"]
        result.casedesc = httpInterfaceDebugData["casedesc"]
        result.businessLineId = TbBusinessLine.objects.get(bussinessLineName=httpInterfaceDebugData["businessLineId"], state=1)
        result.moduleId = TbModules.objects.get(moduleName=httpInterfaceDebugData["moduleId"], state=1)
        result.sourceId = TbSource.objects.get(sourceName=httpInterfaceDebugData["sourceId"], state=1)
        result.caselevel = httpInterfaceDebugData["caselevel"]
        result.status = httpInterfaceDebugData["status"]
        result.caseType = httpInterfaceDebugData["caseType"]
        result.varsPre = httpInterfaceDebugData["varsPre"]
        result.uri = httpInterfaceDebugData["uri"]
        result.method = httpInterfaceDebugData["method"]
        result.header = httpInterfaceDebugData["header"]
        result.url = httpInterfaceDebugData["url"]
        result.params = httpInterfaceDebugData["params"]
        result.bodyType = httpInterfaceDebugData["bodyType"]
        result.bodyContent = httpInterfaceDebugData["bodyContent"]
        result.timeout = httpInterfaceDebugData["timeout"]
        result.varsPost = httpInterfaceDebugData["varsPost"]
        result.performanceTime = httpInterfaceDebugData["performanceTime"]
        result.execStatus = httpInterfaceDebugData["execStatus"]
        result.httpConfKey = TbConfigHttp.objects.get(httpConfKey=httpInterfaceDebugData["httpConfKey"], state=1)
        result.actualResult = httpInterfaceDebugData["actualResult"]
        result.assertResult = httpInterfaceDebugData["assertResult"]
        result.testResult = httpInterfaceDebugData["testResult"]
        result.beforeExecuteTakeTime = httpInterfaceDebugData["beforeExecuteTakeTime"]
        result.afterExecuteTakeTime = httpInterfaceDebugData["afterExecuteTakeTime"]
        result.executeTakeTime = httpInterfaceDebugData["executeTakeTime"]
        result.totalTakeTime = httpInterfaceDebugData["totalTakeTime"]
        result.version = httpInterfaceDebugData["version"]
        result.addBy = TbUser.objects.get(loginName=httpInterfaceDebugData["addBy"].split("(")[1].split(")")[0], state=1)
        result.save()
    except Exception as e:
        message = "编辑接口调试数据发生异常 %s" % e
        logger.info(message)
        return HttpResponse(ApiReturn(code=ApiReturn.CODE_WARNING,message=message).toJson())

    return HttpResponse(ApiReturn().toJson())

def delHttpInterfaceDebug(request):
    httpInterfaceDebugId = request.POST.get("httpInterfaceDebugId","")
    if not httpInterfaceDebugId:
        return HttpResponse(ApiReturn(ApiReturn.CODE_WARNING, message="httpInterfaceDebugId参数错误").toJson())
    try:
        httpInterfaceDebugData = TbHttpInterfaceDebug.objects.get(state=1, id=httpInterfaceDebugId)
    except Exception as e:
        return HttpResponse(ApiReturn(ApiReturn.CODE_WARNING,message="httpInterfaceDebugId查询错误 %s" % e).toJson())
    httpInterfaceDebugData.state = 0
    httpInterfaceDebugData.save()

    return HttpResponse(ApiReturn().toJson())

def resetHttpInterfaceDebug(request):
    httpInterfaceDebugId = request.POST.get("httpInterfaceDebugId", "")
    if not httpInterfaceDebugId:
        return HttpResponse(ApiReturn(ApiReturn.CODE_WARNING, message="httpInterfaceDebugId参数错误").toJson())
    try:
        httpInterfaceDebugData = TbHttpInterfaceDebug.objects.get(state=0, id=httpInterfaceDebugId)
    except Exception as e:
        return HttpResponse(ApiReturn(ApiReturn.CODE_WARNING, message="httpInterfaceDebugId查询错误 %s" % e).toJson())
    httpInterfaceDebugData.state = 1
    httpInterfaceDebugData.save()

    return HttpResponse(ApiReturn().toJson())




