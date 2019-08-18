from urllib import parse

# Create your views here.
from apps.common.config import commonWebConfig
from apps.common.func.WebFunc import *
from apps.myadmin.service.openApiBusinessLineService import OpenApiBusinessLineService
from apps.myadmin.service.openApiUriService import OpenApiUriService

logger = logging.getLogger("django")

def openApiUriCheckPage(request):
    context = {}
    context["openApiUri_check"] = "active"
    return render(request, "myadmin/openAPiUri/admin_openApiUri_check.html", context)

def getOpenApiUri(request):
    checkArr = json.loads(parse.unquote(request.POST.get("checkArr")))
    orderBy = request.POST.get("orderBy", "")
    page = request.POST.get("page")

    if isInt(page):
        page = int(page)
    else:
        addUserLog(request, "单接口管理->查看用例->获取数据->页面参数不合法", "FAIL")
        return HttpResponse("<script>alert('请验证页数参数');</script>")
    execSql = "SELECT u.* from tb_webPortal_openApi_uri u WHERE 1=1 "
    checkList = []
    for key in checkArr:
        if checkArr[key] == "":
            continue
        checkList.append("%%%s%%" % checkArr[key])
        execSql += """ and u.%s """ % key
        execSql += """ LIKE %s"""
    execSql += """ ORDER BY %s""" % orderBy
    context = pagination(sqlStr=execSql,attrList=checkList,page=page,pageNum=commonWebConfig.userPageNum)
    response = render(request, "myadmin/openAPiUri/subPages/openApiUri_sub_page.html",context)
    return response


def getOpenApiUriForId(request):
    openApiUriId = request.POST.get("openApiUriId")
    try:
        openApiUriData = TbOpenApiUri.objects.get(id=openApiUriId)
    except Exception as e:
        message = "openApi_Uri查询出错 %s" % e
        logger.error(message)
        return HttpResponse(ApiReturn(code=ApiReturn.CODE_WARNING, message=message).toJson())
    return HttpResponse(ApiReturn(body=dbModelToDict(openApiUriData)).toJson())


def addOpenApiUri(request):
    openApiUriData = json.loads(request.POST.get("openApiUriData"))
    logger.info("addOpenApiUri %s" % request.POST.get("openApiUriData"))
    summaryUri = openApiUriData["summaryUri"]
    summaryUrl = openApiUriData["summaryUrl"]
    interfaceTestUri = openApiUriData["interfaceTestUri"]
    interfaceTestUrl = openApiUriData["interfaceTestUrl"]
    searchResult = dbModelListToListDict(TbOpenApiUri.objects.filter(summaryUri=summaryUri, summaryUrl=summaryUrl, interfaceTestUri=interfaceTestUri, interfaceTestUrl=interfaceTestUrl))
    if len(searchResult) == 0:
        result = TbOpenApiUri()
        result.summaryUri = summaryUri
        result.summaryUrl = summaryUrl
        result.interfaceTestUri = interfaceTestUri
        result.interfaceTestUrl = interfaceTestUrl
        result.save()
        if result:
            logger.info("addOpenApiUri openApi_Uri创建成功 %s" % result)
        return HttpResponse(ApiReturn().toJson())
    else:

        searchResultDict = searchResult[0]
        if searchResultDict["state"] == 0:
            searchResultDict["state"] = 1
            searchResultDict["summaryUri"] = summaryUri
            searchResultDict["summaryUrl"] = summaryUrl
            searchResultDict["interfaceTestUri"] = interfaceTestUri
            searchResultDict["interfaceTestUrl"] = interfaceTestUrl
            OpenApiBusinessLineService.updatePermission(searchResultDict)
            return HttpResponse(ApiReturn().toJson())
        else:
            logger.info("addOpenApiBusinessLine openApi业务线创建失败")
            return HttpResponse(
                ApiReturn(code=ApiReturn.CODE_WARNING, message="openApi业务线创建失败,请检查数据是否重复").toJson())

    return HttpResponse(ApiReturn().toJson())


def editOpenApiUri(request):
    try:
        openApiUriData =json.loads(request.POST.get("openApiUriData"))
        OpenApiUriService.updateOpenApi(openApiUriData)
    except Exception as e:
        print(traceback.format_exc())
        message = "编辑openApi_Uri发生异常 %s" % e
        logger.info(message)
        return HttpResponse(ApiReturn(code=ApiReturn.CODE_WARNING, message=message).toJson())
    return HttpResponse(ApiReturn().toJson())

def deleteOpenApiUri(request):
    openApiUriId = request.POST.get("openApiUriId", "")
    if not openApiUriId:
        return HttpResponse(ApiReturn(ApiReturn.CODE_WARNING, message="openApiUriId参数错误").toJson())
    try:
        openApiUriData = TbOpenApiUri.objects.get(state=1, id=openApiUriId)
    except Exception as e:
        return HttpResponse(ApiReturn(ApiReturn.CODE_WARNING, message="openApiUriId查询错误 %s" % e).toJson())
    openApiUriData.state = 0
    openApiUriData.save()
    return HttpResponse(ApiReturn().toJson())

def resetOpenApiUri(request):
    openApiUriId = request.POST.get("openApiUriId", "")
    if not openApiUriId:
        return HttpResponse(ApiReturn(ApiReturn.CODE_WARNING, message="openApiUriId参数错误").toJson())
    try:
        openApiUriData = TbOpenApiUri.objects.get(state=0, id=openApiUriId)
    except Exception as e:
        return HttpResponse(ApiReturn(ApiReturn.CODE_WARNING, message="openApiUriId查询错误 %s" % e).toJson())
    openApiUriData.state = 1
    openApiUriData.save()

    return HttpResponse(ApiReturn().toJson())

