from urllib import parse

# Create your views here.
from all_models.models import *
from apps.common.config import commonWebConfig
from apps.common.func.WebFunc import *
from apps.myadmin.service.ConfigService import ConfigService
from apps.myadmin.service.ConfigUriService import ConfigUriService
# from apps.myadmin.service.InterfaceModuleService import InterfaceModuleService

logger = logging.getLogger("django")

def configUriCheckPage(request):
    context = {}
    context["configURI_check"] = "active"
    return render(request, "myadmin/configURI/admin_configURI_check.html",context)

def getConfigUri(request):
    checkArr = json.loads(parse.unquote(request.POST.get("checkArr")))
    orderBy = request.POST.get("orderBy","")
    page = request.POST.get("page")
    if isInt(page):
        page = int(page)
    else:
        addUserLog(request, "单接口管理->查看用例->获取数据->页面参数不合法", "FAIL")
        return HttpResponse("<script>alert('请验证页数参数');</script>")
    execSql = "SELECT u.* from tb_config_uri u WHERE 1=1 "
    checkList = []
    for key in checkArr:
        if checkArr[key] == "":
            continue
        checkList.append("%%%s%%" % checkArr[key])
        execSql += """ and u.%s """ % key
        execSql += """ LIKE %s"""
    execSql += """ ORDER BY %s""" % orderBy
    context = pagination(sqlStr=execSql, attrList=checkList, page=page, pageNum=commonWebConfig.userPageNum)
    response = render(request, "myadmin/configURI/subPages/configURI_sub_page.html", context)
    return response

def getConfigUriForId(request):
    uriKey = request.POST.get("uriKey")
    try:
        configUriData = TbConfigUri.objects.get(uriKey=uriKey)
        requestDict = dbModelToDict(configUriData)
    except Exception as e:
        message = "查询Uri出错 %s" % e
        logger.error(message)
        return HttpResponse(ApiReturn(code=ApiReturn.CODE_WARNING,message=message).toJson())
    return HttpResponse(ApiReturn(body=requestDict).toJson())


def addConfigUri(request):
    configUriData = json.loads(request.POST.get("uriData"))
    logger.info("addConfigUri %s" % request.POST.get("configUriData"))
    searchResult = TbConfigUri.objects.filter(uriKey=configUriData["uriKey"], alias=configUriData["alias"])

    try:
        if len(searchResult) == 0:
            result = TbConfigUri()
            result.uriKey = configUriData["uriKey"]
            result.alias = configUriData["alias"]
            result.uriDesc = configUriData["uriDesc"]
            result.level = configUriData["level"]
            result.protocol = configUriData["protocol"]
            result.save()
            if result:
                logger.info("addConfigUri uri添加成功 %s" % result)
            return HttpResponse(ApiReturn().toJson())
        else:
            if searchResult.state == 0:
                searchResult.state = 1
                searchResult.save()
                return HttpResponse(ApiReturn().toJson())
            else:
                logger.info("addConfigUri uri添加失败")
                return HttpResponse(ApiReturn(code=ApiReturn.CODE_WARNING, message="uri添加失败,请检查账号是否重复").toJson())
    except Exception as e:
        message = "uri添加失败 :%s" % e
        logger.info(message)
        return HttpResponse(ApiReturn(code=ApiReturn.CODE_WARNING, message="uri添加失败,请检查账号是否重复").toJson())


def editConfigUri(request):
    try:
        requestDict = json.loads(request.POST.get("uriData"))
        ConfigUriService.updateConfigUri(requestDict)
    except Exception as e:
        message = "编辑uri发生异常 %s" % e
        logger.info(message)
        return HttpResponse(ApiReturn(code=ApiReturn.CODE_WARNING,message=message).toJson())

    return HttpResponse(ApiReturn().toJson())

def delConfigUri(request):
    uriKey = request.POST.get("uriKey","")
    if not uriKey:
        return HttpResponse(ApiReturn(ApiReturn.CODE_WARNING,message="uriKey参数错误").toJson())
    try:
        configUriData = TbConfigUri.objects.get(state=1, uriKey=uriKey)
    except Exception as e:
        return HttpResponse(ApiReturn(ApiReturn.CODE_WARNING,message="uriKey查询错误 %s" % e).toJson())
    configUriData.state = 0
    configUriData.save()

    return HttpResponse(ApiReturn().toJson())

def resetConfigUri(request):
    uriKey = request.POST.get("uriKey", "")
    if not uriKey:
        return HttpResponse(ApiReturn(ApiReturn.CODE_WARNING,message="uriKey参数错误").toJson())
    try:
        configUriData = TbConfigUri.objects.get(state=0, uriKey=uriKey)
    except Exception as e:
        return HttpResponse(ApiReturn(ApiReturn.CODE_WARNING,message="configUriId查询错误 %s" % e).toJson())
    configUriData.state = 1
    configUriData.save()

    return HttpResponse(ApiReturn().toJson())
