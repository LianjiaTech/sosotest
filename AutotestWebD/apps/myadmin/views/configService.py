from urllib import parse

# Create your views here.
from all_models.models import *
from apps.common.config import commonWebConfig
from apps.common.func.WebFunc import *
from apps.myadmin.service.ConfigService import ConfigService
# from apps.myadmin.service.InterfaceModuleService import InterfaceModuleService

logger = logging.getLogger("django")

def configServiceCheckPage(request):
    context = {}
    context["configService_check"] = "active"
    return render(request, "myadmin/configService/admin_configService_check.html",context)

def getConfigService(request):
    checkArr = json.loads(parse.unquote(request.POST.get("checkArr")))
    orderBy = request.POST.get("orderBy","")
    page = request.POST.get("page")
    if isInt(page):
        page = int(page)
    else:
        addUserLog(request, "单接口管理->查看用例->获取数据->页面参数不合法", "FAIL")
        return HttpResponse("<script>alert('请验证页数参数');</script>")
    execSql = "SELECT u.* from tb_config_service u WHERE 1=1 "
    checkList = []
    for key in checkArr:
        if checkArr[key] == "":
            continue
        checkList.append("%%%s%%" % checkArr[key])
        execSql += """ and u.%s """ % key
        execSql += """ LIKE %s"""
    execSql += """ ORDER BY %s""" % orderBy
    context = pagination(sqlStr=execSql,attrList=checkList,page=page,pageNum=commonWebConfig.userPageNum)
    response = render(request, "myadmin/configService/subPages/configService_sub_page.html",context)
    return response

def getConfigServiceForId(request):
    configServiceId = request.POST.get("configServiceId")
    try:
        configServiceData = TbConfigService.objects.get(id=configServiceId)
        requestDict = dbModelToDict(configServiceData)
    except Exception as e:
        message = "查询数据服务器出错 %s" % e
        logger.error(message)
        return HttpResponse(ApiReturn(code=ApiReturn.CODE_WARNING,message=message).toJson())
    return HttpResponse(ApiReturn(body=requestDict).toJson())


def addConfigService(request):
    configServiceData = json.loads(request.POST.get("configServiceData"))
    logger.info("addconfigService %s" % request.POST.get("configServiceData"))
    searchResult = TbConfigService.objects.filter(serviceConfKey=configServiceData["serviceConfKey"], alias=configServiceData["alias"])
    if not isJson(configServiceData["serviceConf"]):
        return HttpResponse(ApiReturn(code=ApiReturn.CODE_WARNING, message="配置文件必须为json格式").toJson())
    try:
        if len(searchResult) == 0:
            result = TbConfigService()
            result.serviceConfKey = configServiceData["serviceConfKey"]
            result.alias = configServiceData["alias"]
            result.serviceConfDesc = configServiceData["serviceConfDesc"]
            result.serviceConf = configServiceData["serviceConf"]
            result.save()
            if result:
                logger.info("addConfigService 数据服务器添加成功 %s" % result)
            return HttpResponse(ApiReturn().toJson())
        else:
            if searchResult.state == 0:
                searchResult.state = 1
                searchResult.save()
                return HttpResponse(ApiReturn().toJson())
            else:
                logger.info("addConfigService 数据服务器添加失败")
                return HttpResponse(ApiReturn(code=ApiReturn.CODE_WARNING, message="数据服务器添加失败,请检查账号是否重复").toJson())
    except Exception as e:
        message = "数据服务器添加失败 :%s" % e
        logger.info(message)
        return HttpResponse(ApiReturn(code=ApiReturn.CODE_WARNING, message="数据服务器添加失败,请检查账号是否重复").toJson())


def editConfigService(request):
    try:
        requestDict = json.loads(request.POST.get("configServiceData"))
        requestDict["modBy"] = request.session.get("userName")
        if not isJson(requestDict["serviceConf"]):
            return HttpResponse(ApiReturn(code=ApiReturn.CODE_WARNING, message="配置文件必须为json格式").toJson())
        ConfigService.updateConfigService(requestDict)
    except Exception as e:
        message = "编辑数据服务器发生异常 %s" % e
        logger.info(message)
        return HttpResponse(ApiReturn(code=ApiReturn.CODE_WARNING,message=message).toJson())

    return HttpResponse(ApiReturn().toJson())

def delConfigService(request):
    configServiceId = request.POST.get("configServiceId","")
    if not configServiceId:
        return HttpResponse(ApiReturn(ApiReturn.CODE_WARNING,message="configServiceId参数错误").toJson())
    try:
        configServiceData = TbConfigService.objects.get(state=1, id=configServiceId)
    except Exception as e:
        return HttpResponse(ApiReturn(ApiReturn.CODE_WARNING,message="configServiceId查询错误 %s" % e).toJson())
    configServiceData.state = 0
    configServiceData.save()

    return HttpResponse(ApiReturn().toJson())

def resetConfigService(request):
    configServiceId = request.POST.get("configServiceId","")
    if not configServiceId:
        return HttpResponse(ApiReturn(ApiReturn.CODE_WARNING,message="configServiceId参数错误").toJson())
    try:
        configServiceData = TbConfigService.objects.get(state=0, id=configServiceId)
    except Exception as e:
        return HttpResponse(ApiReturn(ApiReturn.CODE_WARNING,message="configServiceId查询错误 %s" % e).toJson())
    configServiceData.state = 1
    configServiceData.save()

    return HttpResponse(ApiReturn().toJson())
