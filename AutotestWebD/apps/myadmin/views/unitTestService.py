from urllib import parse

# Create your views here.
from apps.common.config import commonWebConfig
from apps.common.func.WebFunc import *
from apps.myadmin.service.UnitTestService import UnitTestService

logger = logging.getLogger("django")

def unitTestServiceCheckPage(request):
    context = {}
    context["unitTestService_check"] = "active"
    return render(request, "myadmin/unitTestService/admin_unitTestService_check.html", context)

def getUnitTestService(request):
    checkArr = json.loads(parse.unquote(request.POST.get("checkArr")))
    orderBy = request.POST.get("orderBy", "")
    page = request.POST.get("page")

    if isInt(page):
        page = int(page)
    else:
        addUserLog(request, "单接口管理->查看用例->获取数据->页面参数不合法", "FAIL")
        return HttpResponse("<script>alert('请验证页数参数');</script>")
    execSql = "SELECT u.* from tb_webPortal_unit_test_service u WHERE 1=1 "
    checkList = []
    for key in checkArr:
        if checkArr[key] == "":
            continue
        checkList.append("%%%s%%" % checkArr[key])
        execSql += """ and u.%s """ % key
        execSql += """ LIKE %s"""
    execSql += """ ORDER BY %s""" % orderBy
    context = pagination(sqlStr=execSql,attrList=checkList,page=page,pageNum=commonWebConfig.userPageNum)
    response = render(request, "myadmin/unitTestService/subPages/unitTestService_sub_page.html",context)
    return response


def getUnitTestServiceForId(request):
    unitTestServiceId = request.POST.get("unitTestServiceId")
    try:
        unitTestServiceData = TbWebPortalUnitTestService.objects.get(id=unitTestServiceId)
    except Exception as e:
        message = "unitTestService查询出错 %s" % e
        logger.error(message)
        return HttpResponse(ApiReturn(code=ApiReturn.CODE_WARNING, message=message).toJson())
    return HttpResponse(ApiReturn(body=dbModelToDict(unitTestServiceData)).toJson())


def addUnitTestService(request):
    unitTestServiceData = json.loads(request.POST.get("unitTestServiceData"))
    logger.info("unitTestServiceData %s" % request.POST.get("unitTestServiceData"))
    serviceName = unitTestServiceData["serviceName"]
    serviceDesc = unitTestServiceData["serviceDesc"]
    isShow = unitTestServiceData["isShow"]
    level = unitTestServiceData["level"]
    searchResult = dbModelListToListDict(TbWebPortalUnitTestService.objects.filter(serviceName=serviceName))
    if len(searchResult) == 0:
        result = TbWebPortalUnitTestService()
        result.serviceName = serviceName
        result.serviceDesc = serviceDesc
        result.isShow = isShow
        result.level = level
        result.save()
        if result:
            logger.info("addUnitTestService unitTestService创建成功 %s" % result)
        return HttpResponse(ApiReturn().toJson())
    else:
        searchResultDict = searchResult[0]
        if searchResultDict["state"] == 0:
            searchResultDict["state"] = 1
            searchResultDict["serviceName"] = serviceName
            searchResultDict["serviceDesc"] = serviceDesc
            searchResultDict["isShow"] = isShow
            searchResultDict["level"] = level
            UnitTestService.updataUnitTestService(searchResultDict)
            return HttpResponse(ApiReturn().toJson())
        else:
            logger.info("addUnitTestService unitTestService创建失败")
            return HttpResponse(
                ApiReturn(code=ApiReturn.CODE_WARNING, message="unitTestService创建失败,请检查数据是否重复").toJson())

    return HttpResponse(ApiReturn().toJson())


def editUnitTestService(request):
    try:
        unitTestServiceData =json.loads(request.POST.get("unitTestServiceData"))
        UnitTestService.updataUnitTestService(unitTestServiceData)
    except Exception as e:
        print(traceback.format_exc())
        message = "编辑unitTestService发生异常 %s" % e
        logger.info(message)
        return HttpResponse(ApiReturn(code=ApiReturn.CODE_WARNING, message=message).toJson())
    return HttpResponse(ApiReturn().toJson())

def deleteUnitTestService(request):
    unitTestServiceId = request.POST.get("unitTestServiceId", "")
    if not unitTestServiceId:
        return HttpResponse(ApiReturn(ApiReturn.CODE_WARNING, message="unitTestServiceId参数错误").toJson())
    try:
        unitTestServiceData = TbWebPortalUnitTestService.objects.get(state=1, id=unitTestServiceId)
    except Exception as e:
        return HttpResponse(ApiReturn(ApiReturn.CODE_WARNING, message="unitTestServiceId查询错误 %s" % e).toJson())
    unitTestServiceData.state = 0
    unitTestServiceData.save()
    return HttpResponse(ApiReturn().toJson())

def resetUnitTestService(request):
    unitTestServiceId = request.POST.get("unitTestServiceId", "")
    if not unitTestServiceId:
        return HttpResponse(ApiReturn(ApiReturn.CODE_WARNING, message="unitTestServiceId参数错误").toJson())
    try:
        unitTestServiceData = TbWebPortalUnitTestService.objects.get(state=0, id=unitTestServiceId)
    except Exception as e:
        return HttpResponse(ApiReturn(ApiReturn.CODE_WARNING, message="unitTestServiceId查询错误 %s" % e).toJson())
    unitTestServiceData.state = 1
    unitTestServiceData.save()

    return HttpResponse(ApiReturn().toJson())

