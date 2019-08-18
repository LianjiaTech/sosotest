from urllib import parse

# Create your views here.
from all_models.models import *
from apps.common.config import commonWebConfig
from apps.common.func.WebFunc import *
from apps.myadmin.service.ConfigHttpService import ConfigHttpService



logger = logging.getLogger("django")

def configHttpCheckPage(request):
    context = {}
    context["configHttp_check"] = "active"
    return render(request, "myadmin/configHttp/admin_configHttp_check.html",context)

def getConfigHttp(request):
    checkArr = json.loads(parse.unquote(request.POST.get("checkArr")))

    orderBy = request.POST.get("orderBy","")
    page = request.POST.get("page")
    if isInt(page):
        page = int(page)
    else:
        addUserLog(request, "单接口管理->查看用例->获取数据->页面参数不合法", "FAIL")
        return HttpResponse("<script>alert('请验证页数参数');</script>")
    execSql = "SELECT u.* from tb_config_http u WHERE 1=1 "
    checkList = []
    for key in checkArr:
        if checkArr[key] == "":
            continue
        checkList.append("%%%s%%" % checkArr[key])
        execSql += """ and u.%s """ % key
        execSql += """ LIKE %s"""
    execSql += """ ORDER BY %s""" % orderBy
    context = pagination(sqlStr=execSql, attrList=checkList, page=page, pageNum=commonWebConfig.userPageNum)
    response = render(request, "myadmin/configHttp/subPages/configHttp_sub_page.html", context)
    return response

def getConfigHttpForId(request):
    configHttpId = request.POST.get("configHttpId")
    try:
        configHttpData = TbConfigHttp.objects.get(id=configHttpId)
        requestDict = dbModelToDict(configHttpData)
        del requestDict["serviceConfKey_id"]
        requestDict["serviceConfKey"] = configHttpData.serviceConfKey.serviceConfKey
    except Exception as e:
        message = "查询环境配置出错 %s" % e
        logger.error(message)
        return HttpResponse(ApiReturn(code=ApiReturn.CODE_WARNING, message=message).toJson())
    return HttpResponse(ApiReturn(body=requestDict).toJson())


def addConfigHttp(request):
    configHttpData = json.loads(request.POST.get("configHttpData"))
    logger.info("addConfigHttp %s" % request.POST.get("configHttpData"))
    searchResult = TbConfigHttp.objects.filter(httpConfKey=configHttpData["httpConfKey"], alias=configHttpData["alias"])

    try:
        if len(searchResult) == 0:
            result = TbConfigHttp()
            result.httpConfKey = configHttpData["httpConfKey"]
            serviceConf = TbConfigService.objects.get(serviceConfKey=configHttpData["serviceConfKey"], state=1)
            result.serviceConfKey = serviceConf
            result.alias = configHttpData["alias"]
            result.httpConfDesc = configHttpData["httpConfDesc"]
            result.apiRunState = configHttpData["apiRunState"]
            result.uiRunState = configHttpData["uiRunState"]
            result.dubboRunState = configHttpData["dubboRunState"]
            result.save()
            if result:
                logger.info("addConfigHttp 环境配置添加成功 %s" % result)
            return HttpResponse(ApiReturn().toJson())
        else:
            if searchResult.state == 0:
                searchResult.state = 1
                searchResult.save()
                return HttpResponse(ApiReturn().toJson())
            else:
                logger.info("addConfigHttp 环境配置添加失败")
                return HttpResponse(ApiReturn(code=ApiReturn.CODE_WARNING, message="环境配置添加失败,请检查账号是否重复").toJson())
    except Exception as e:
        print(traceback.format_exc())
        message = "环境配置添加失败 :%s" % e
        logger.info(message)
        return HttpResponse(ApiReturn(code=ApiReturn.CODE_WARNING, message="环境配置添加失败,请检查账号是否重复").toJson())


def editConfigHttp(request):
    try:
        requestDict = json.loads(request.POST.get("configHttpData"))
        ConfigHttpService.updateConfigHttp(requestDict)
    except Exception as e:
        message = "编辑数据服务器发生异常 %s" % e
        logger.info(message)
        return HttpResponse(ApiReturn(code=ApiReturn.CODE_WARNING,message=message).toJson())

    return HttpResponse(ApiReturn().toJson())

def delConfigHttp(request):
    configHttpId = request.POST.get("configHttpId","")
    if not configHttpId:
        return HttpResponse(ApiReturn(ApiReturn.CODE_WARNING, message="configHttpId参数错误").toJson())
    try:
        configHttpData = TbConfigHttp.objects.get(state=1, id=configHttpId)
    except Exception as e:
        return HttpResponse(ApiReturn(ApiReturn.CODE_WARNING,message="configHttpId查询错误 %s" % e).toJson())
    configHttpData.state = 0
    configHttpData.save()

    return HttpResponse(ApiReturn().toJson())

def resetConfigHttp(request):
    configHttpId = request.POST.get("configHttpId", "")
    if not configHttpId:
        return HttpResponse(ApiReturn(ApiReturn.CODE_WARNING, message="configHttpId参数错误").toJson())
    try:
        configHttpData = TbConfigHttp.objects.get(state=0, id=configHttpId)
    except Exception as e:
        return HttpResponse(ApiReturn(ApiReturn.CODE_WARNING, message="configHttpId查询错误 %s" % e).toJson())
    configHttpData.state = 1
    configHttpData.save()

    return HttpResponse(ApiReturn().toJson())

def getAllServiceConfKeys(request):
    configServices = TbConfigService.objects.filter(state=1)
    if len(configServices) == 0:
        return HttpResponse(ApiReturn(code=ApiReturn.CODE_WARNING, message="没有可选择的服务配置").toJson())
    serviceConfKeysList = []
    for configService in configServices:
        serviceConfKeysList.append(configService.serviceConfKey)
    return HttpResponse(ApiReturn(body=serviceConfKeysList).toJson())
