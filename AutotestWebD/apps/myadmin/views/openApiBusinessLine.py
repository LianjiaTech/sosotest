from urllib import parse

# Create your views here.
from apps.common.config import commonWebConfig
from apps.common.func.WebFunc import *
from apps.myadmin.service.openApiBusinessLineService import OpenApiBusinessLineService

logger = logging.getLogger("django")

def openApiBusinessLineCheckPage(request):
    context = {}
    context["openApiBusinessLine_check"] = "active"
    return render(request, "myadmin/openApiBusinessLine/admin_openApiBusinessLine_check.html", context)

def getOpenApiBusinessLine(request):
    checkArr = json.loads(parse.unquote(request.POST.get("checkArr")))
    orderBy = request.POST.get("orderBy", "")
    page = request.POST.get("page")

    if isInt(page):
        page = int(page)
    else:
        addUserLog(request, "单接口管理->查看用例->获取数据->页面参数不合法", "FAIL")
        return HttpResponse("<script>alert('请验证页数参数');</script>")
    execSql = "SELECT u.* from tb_webPortal_openApi_businessLine u WHERE 1=1 "
    checkList = []
    for key in checkArr:
        if checkArr[key] == "":
            continue
        checkList.append("%%%s%%" % checkArr[key])
        execSql += """ and u.%s """ % key
        execSql += """ LIKE %s"""
    execSql += """ ORDER BY %s""" % orderBy
    context = pagination(sqlStr=execSql,attrList=checkList,page=page,pageNum=commonWebConfig.userPageNum)
    response = render(request, "myadmin/openApiBusinessLine/subPages/openApiBusinessLine_sub_page.html",context)
    return response


def getOpenApiBusinessLineForId(request):
    openApiBusinessLineId = request.POST.get("openApiBusinessLineId")
    try:
        openApiBusinessLineData = TbOpenApiBusinessLine.objects.get(id=openApiBusinessLineId)
    except Exception as e:
        message = "openApi业务线查询出错 %s" % e
        logger.error(message)
        return HttpResponse(ApiReturn(code=ApiReturn.CODE_WARNING, message=message).toJson())
    return HttpResponse(ApiReturn(body=dbModelToDict(openApiBusinessLineData)).toJson())


def addOpenApiBusinessLine(request):
    openApiBusinessLineData = json.loads(request.POST.get("openApiBusinessLineData"))
    logger.info("addOpenApiBusinessLine %s" % request.POST.get("openApiBusinessLineData"))
    businessLineName = openApiBusinessLineData["businessLineName"]
    businessLineDesc = openApiBusinessLineData["businessLineDesc"]
    searchResult = dbModelListToListDict(TbOpenApiBusinessLine.objects.filter(businessLineName=businessLineName))
    if len(searchResult) == 0:
        result = TbOpenApiBusinessLine()
        result.businessLineName = businessLineName
        result.businessLineDesc = businessLineDesc
        result.save()
        if result:
            logger.info("addOpenApiBusinessLine openApi业务线创建成功 %s" % result)
        return HttpResponse(ApiReturn().toJson())
    else:

        searchResultDict = searchResult[0]
        if searchResultDict["state"] == 0:
            searchResultDict["state"] = 1
            searchResultDict["businessLineName"] = businessLineName
            searchResultDict["businessLineDesc"] = businessLineDesc
            OpenApiBusinessLineService.updatePermission(searchResultDict)
            return HttpResponse(ApiReturn().toJson())
        else:
            logger.info("addOpenApiBusinessLine openApi业务线创建失败")
            return HttpResponse(
                ApiReturn(code=ApiReturn.CODE_WARNING, message="openApi业务线创建失败,请检查数据是否重复").toJson())

    return HttpResponse(ApiReturn().toJson())


def editOpenApiBusinessLine(request):
    try:
        openApiBusinessLineData =json.loads(request.POST.get("openApiBusinessLineData"))
        OpenApiBusinessLineService.updatePermission(openApiBusinessLineData)
    except Exception as e:
        print(traceback.format_exc())
        message = "编辑openApi业务线发生异常 %s" % e
        logger.info(message)
        return HttpResponse(ApiReturn(code=ApiReturn.CODE_WARNING, message=message).toJson())
    return HttpResponse(ApiReturn().toJson())

def delOpenApiBusinessLine(request):
    openApiBusinessLineId = request.POST.get("openApiBusinessLineId", "")
    if not openApiBusinessLineId:
        return HttpResponse(ApiReturn(ApiReturn.CODE_WARNING, message="openApiBusinessLineId参数错误").toJson())
    try:
        openApiBusinessLineData = TbOpenApiBusinessLine.objects.get(state=1, id=openApiBusinessLineId)
    except Exception as e:
        return HttpResponse(ApiReturn(ApiReturn.CODE_WARNING, message="openApiBusinessLineId查询错误 %s" % e).toJson())
    openApiBusinessLineData.state = 0
    openApiBusinessLineData.save()
    return HttpResponse(ApiReturn().toJson())

def resetOpenApiBusinessLine(request):
    openApiBusinessLineId = request.POST.get("openApiBusinessLineId", "")
    if not openApiBusinessLineId:
        return HttpResponse(ApiReturn(ApiReturn.CODE_WARNING, message="openApiBusinessLineId参数错误").toJson())
    try:
        openApiBusinessLineData = TbOpenApiBusinessLine.objects.get(state=0, id=openApiBusinessLineId)
    except Exception as e:
        return HttpResponse(ApiReturn(ApiReturn.CODE_WARNING, message="openApiBusinessLineId查询错误 %s" % e).toJson())
    openApiBusinessLineData.state = 1
    openApiBusinessLineData.save()

    return HttpResponse(ApiReturn().toJson())

