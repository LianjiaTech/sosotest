from urllib import parse

# Create your views here.
from all_models.models import *
from apps.common.config import commonWebConfig
from apps.common.func.WebFunc import *
from apps.myadmin.service.ConfigHttpService import ConfigHttpService
from apps.myadmin.service.HttpInterfaceDebugService import HttpInterfaceDebugService

logger = logging.getLogger("django")

def httpTestcaseDebugCheckPage(request):
    context = {}
    context["httpTestcaseDebug_check"] = "active"
    return render(request, "myadmin/httpTestcaseDebug/admin_httpTestcaseDebug_check.html",context)

def getHttpTestcaseDebug(request):
    checkArr = json.loads(parse.unquote(request.POST.get("checkArr")))

    orderBy = request.POST.get("orderBy","")
    page = request.POST.get("page")
    if isInt(page):
        page = int(page)
    else:
        addUserLog(request, "单接口管理->查看用例->获取数据->页面参数不合法", "FAIL")
        return HttpResponse("<script>alert('请验证页数参数');</script>")
    execSql = "SELECT u.* from tb_http_testcase_debug u WHERE 1=1 "
    checkList = []
    for key in checkArr:
        if checkArr[key] == "":
            continue
        checkList.append("%%%s%%" % checkArr[key])
        execSql += """ and u.%s """ % key
        execSql += """ LIKE %s"""
    execSql += """ ORDER BY %s""" % orderBy
    context = pagination(sqlStr=execSql, attrList=checkList, page=page, pageNum=commonWebConfig.userPageNum)
    response = render(request, "myadmin/httpTestcaseDebug/subPages/httpTestcaseDebug_sub_page.html", context)
    return response

def getHttpTestcaseDebugForId(request):
    httpTestcaseDebugId = request.POST.get("httpTestcaseDebugId")
    try:
        httpTestcaseDebugData = TbHttpTestcaseDebug.objects.get(id=httpTestcaseDebugId)
        requestDict = dbModelToDict(httpTestcaseDebugData)
        del requestDict["businessLineId_id"]
        requestDict["businessLineId"] = httpTestcaseDebugData.businessLineId.bussinessLineName
        del requestDict["moduleId_id"]
        requestDict["moduleId"] = httpTestcaseDebugData.moduleId.moduleName
        del requestDict["sourceId_id"]
        requestDict["sourceId"] = httpTestcaseDebugData.sourceId.sourceName
        del requestDict["httpConfKey_id"]
        requestDict["httpConfKey"] = httpTestcaseDebugData.httpConfKey.httpConfKey
        del requestDict["addBy_id"]
        requestDict["addBy"] = httpTestcaseDebugData.addBy.userName + "(" + httpTestcaseDebugData.addBy.loginName + ")"

    except Exception as e:
        message = "查询接口用例调试数据出错 %s" % e
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

def addHttpTestcaseDebug(request):
    httpTestcaseDebugData = json.loads(request.POST.get("httpTestcaseDebugData"))
    logger.info("addHttpTestcaseDebug %s" % request.POST.get("httpTestcaseDebugData"))
    searchResult = TbHttpTestcaseDebug.objects.filter(caseId=httpTestcaseDebugData["caseId"])
    try:
        if len(searchResult) == 0:
            result = TbHttpTestcaseDebug()
            result.caseId = httpTestcaseDebugData["caseId"]
            result.title = httpTestcaseDebugData["title"]
            result.casedesc = httpTestcaseDebugData["casedesc"]
            result.businessLineId = TbBusinessLine.objects.get(bussinessLineName=httpTestcaseDebugData["businessLineId"], state=1)
            result.moduleId = TbModules.objects.get(moduleName=httpTestcaseDebugData["moduleId"], state=1)
            result.sourceId = TbSource.objects.get(sourceName=httpTestcaseDebugData["sourceId"], state=1)
            result.caselevel = httpTestcaseDebugData["caselevel"]
            result.status = httpTestcaseDebugData["status"]
            result.stepCount = httpTestcaseDebugData["stepCount"]
            result.caseType = httpTestcaseDebugData["caseType"]
            result.execStatus = httpTestcaseDebugData["execStatus"]
            result.httpConfKey = TbConfigHttp.objects.get(httpConfKey=httpTestcaseDebugData["httpConfKey"], state=1)
            result.assertResult = httpTestcaseDebugData["assertResult"]
            result.testResult = httpTestcaseDebugData["testResult"]
            result.beforeExecuteTakeTime = httpTestcaseDebugData["beforeExecuteTakeTime"]
            result.afterExecuteTakeTime = httpTestcaseDebugData["afterExecuteTakeTime"]
            result.executeTakeTime = httpTestcaseDebugData["executeTakeTime"]
            result.totalTakeTime = httpTestcaseDebugData["totalTakeTime"]
            result.version = httpTestcaseDebugData["version"]
            result.addBy = TbUser.objects.get(loginName=httpTestcaseDebugData["addBy"].split("(")[1].split(")")[0], state=1)
            result.save()
            if result:
                logger.info("addHttpTestcaseDebug 接口用例调试添加成功 %s" % result)
            return HttpResponse(ApiReturn().toJson())
        else:
            if searchResult.state == 0:
                searchResult.state = 1
                searchResult.save()
                return HttpResponse(ApiReturn().toJson())
            else:
                logger.info("addHttpTestcaseDebug 接口用例调试添加失败")
                return HttpResponse(ApiReturn(code=ApiReturn.CODE_WARNING, message="接口用例调试添加失败,请检查账号是否重复").toJson())
    except Exception as e:
        message = "接口用例调试添加失败 :%s" % e
        logger.info(message)
        return HttpResponse(ApiReturn(code=ApiReturn.CODE_WARNING, message="接口用例调试添加失败,请检查账号是否重复").toJson())


def editHttpTestcaseDebug(request):
    try:
        httpTestcaseDebugData = json.loads(request.POST.get("httpTestcaseDebugData"))
        result = TbHttpTestcaseDebug.objects.get(id=httpTestcaseDebugData["id"])
        result.caseId = httpTestcaseDebugData["caseId"]
        result.title = httpTestcaseDebugData["title"]
        result.casedesc = httpTestcaseDebugData["casedesc"]
        result.businessLineId = TbBusinessLine.objects.get(bussinessLineName=httpTestcaseDebugData["businessLineId"], state=1)
        result.moduleId = TbModules.objects.get(moduleName=httpTestcaseDebugData["moduleId"], state=1)
        result.sourceId = TbSource.objects.get(sourceName=httpTestcaseDebugData["sourceId"], state=1)
        result.caselevel = httpTestcaseDebugData["caselevel"]
        result.status = httpTestcaseDebugData["status"]
        result.stepCount = httpTestcaseDebugData["stepCount"]
        result.caseType = httpTestcaseDebugData["caseType"]
        result.execStatus = httpTestcaseDebugData["execStatus"]
        result.httpConfKey = TbConfigHttp.objects.get(httpConfKey=httpTestcaseDebugData["httpConfKey"], state=1)
        result.assertResult = httpTestcaseDebugData["assertResult"]
        result.testResult = httpTestcaseDebugData["testResult"]
        result.beforeExecuteTakeTime = httpTestcaseDebugData["beforeExecuteTakeTime"]
        result.afterExecuteTakeTime = httpTestcaseDebugData["afterExecuteTakeTime"]
        result.executeTakeTime = httpTestcaseDebugData["executeTakeTime"]
        result.totalTakeTime = httpTestcaseDebugData["totalTakeTime"]
        result.version = httpTestcaseDebugData["version"]
        result.addBy = TbUser.objects.get(loginName=httpTestcaseDebugData["addBy"].split("(")[1].split(")")[0], state=1)
        result.save()
    except Exception as e:
        message = "编辑接口用例调试数据发生异常 %s" % e
        logger.info(message)
        return HttpResponse(ApiReturn(code=ApiReturn.CODE_WARNING,message=message).toJson())

    return HttpResponse(ApiReturn().toJson())

def delHttpTestcaseDebug(request):
    httpTestcaseDebugId = request.POST.get("httpTestcaseDebugId", "")
    if not httpTestcaseDebugId:
        return HttpResponse(ApiReturn(ApiReturn.CODE_WARNING, message="httpTestcaseDebugId参数错误").toJson())
    try:
        httpTestcaseDebugData = TbHttpTestcaseDebug.objects.get(state=1, id=httpTestcaseDebugId)
    except Exception as e:
        return HttpResponse(ApiReturn(ApiReturn.CODE_WARNING,message="httpTestcaseDebugId查询错误 %s" % e).toJson())
    httpTestcaseDebugData.state = 0
    httpTestcaseDebugData.save()

    return HttpResponse(ApiReturn().toJson())

def resetHttpTestcaseDebug(request):
    httpTestcaseDebugId = request.POST.get("httpTestcaseDebugId", "")
    if not httpTestcaseDebugId:
        return HttpResponse(ApiReturn(ApiReturn.CODE_WARNING, message="httpTestcaseDebugId参数错误").toJson())
    try:
        httpTestcaseDebugData = TbHttpTestcaseDebug.objects.get(state=0, id=httpTestcaseDebugId)
    except Exception as e:
        return HttpResponse(ApiReturn(ApiReturn.CODE_WARNING, message="httpTestcaseDebugId查询错误 %s" % e).toJson())
    httpTestcaseDebugData.state = 1
    httpTestcaseDebugData.save()

    return HttpResponse(ApiReturn().toJson())




