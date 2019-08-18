from urllib import parse

# Create your views here.
from all_models.models import *
from apps.common.config import commonWebConfig
from apps.common.func.WebFunc import *
from apps.myadmin.service.ExePythonService import ExePythonService
# from apps.myadmin.service.InterfaceModuleService import InterfaceModuleService
from apps.myadmin.service.InterfacePermissionService import InterfacePermissionService
from apps.myadmin.service.ModuleService import ModuleService
from apps.myadmin.service.UserPermissionRelationService import UserPermissionRelationService
from apps.myadmin.service.UserService import UserService
from apps.common.model.RedisDBConfig import RedisCache

logger = logging.getLogger("django")

def exePythonCheckPage(request):
    context = {}
    context["exePython_check"] = "active"
    return render(request, "myadmin/exePython/admin_exePython_check.html",context)

def getExePython(request):
    checkArr = json.loads(parse.unquote(request.POST.get("checkArr")))
    orderBy = request.POST.get("orderBy","")
    page = request.POST.get("page")
    if isInt(page):
        page = int(page)
    else:
        return HttpResponse("<script>alert('请验证页数参数');</script>")
    execSql = "SELECT u.* from tb_exec_python_attrs u WHERE 1=1 "
    checkList = []
    for key in checkArr:
        if checkArr[key] == "":
            continue
        checkList.append("%%%s%%" % checkArr[key])
        execSql += """ and u.%s """ % key
        execSql += """ LIKE %s"""
    execSql += """ ORDER BY %s""" % orderBy
    context = pagination(sqlStr=execSql,attrList=checkList,page=page,pageNum=commonWebConfig.userPageNum)
    response = render(request, "myadmin/exePython/subPages/exePython_sub_page.html",context)
    return response

def getExePythonForId(request):
    exePythonId = request.POST.get("exePythonId")
    try:
        exePythonData = TbExecPythonAttrs.objects.get(id=exePythonId)
        requestDict = dbModelToDict(exePythonData)
    except Exception as e:
        message = "查询执行python代码出错 %s" % e
        logger.error(message)
        return HttpResponse(ApiReturn(code=ApiReturn.CODE_WARNING,message=message).toJson())
    return HttpResponse(ApiReturn(body=requestDict).toJson())


def addExePython(request):
    exePythonRequest = json.loads(request.POST.get("exePythonData"))
    logger.info("addInterfacePermission %s" % request.POST.get("interfacePermissionData"))
    exePythonRequest["addTime"] = datetime.datetime.now()
    searchResult = dbModelListToListDict(TbExecPythonAttrs.objects.filter(execPythonAttr=exePythonRequest["execPythonAttr"]))

    try:
        if len(searchResult) == 0:
            result = TbExecPythonAttrs()
            result.execPythonAttr = exePythonRequest["execPythonAttr"]
            result.execPythonDesc = exePythonRequest["execPythonDesc"]
            result.execPythonValue = exePythonRequest["execPythonValue"]
            result.save()
            if result:
                logger.info("addModuleManage 模块添加成功 %s" % result)
            return HttpResponse(ApiReturn().toJson())
        else:
            searchData = searchResult[0]
            if searchData["state"] == 0:
                searchData["state"] = 1
                searchData["execPythonDesc"] = exePythonRequest["execPythonDesc"]
                searchData["execPythonValue"] = exePythonRequest["execPythonValue"]
                ExePythonService.updateModule(searchData)
                return HttpResponse(ApiReturn().toJson())
            else:
                logger.info("addModuleManage python代码执行创建失败")
                return HttpResponse(ApiReturn(code=ApiReturn.CODE_WARNING, message="python代码执行创建失败,请检查账号是否重复").toJson())
    except Exception as e:
        message = "添加python代码执行失败 :%s" % e
        logger.info(message)
        return HttpResponse(ApiReturn(code=ApiReturn.CODE_WARNING, message="python代码执行创建失败,请检查账号是否重复").toJson())


def editExePython(request):
    try:
        requestDict = json.loads(request.POST.get("exePythonData"))
        ExePythonService.updateModule(requestDict)

    except Exception as e:
        print(traceback.format_exc())
        message = "编辑模块发生异常 %s" % e
        logger.info(message)
        return HttpResponse(ApiReturn(code=ApiReturn.CODE_WARNING,message=message).toJson())

    return HttpResponse(ApiReturn().toJson())

def delExePython(request):
    exePythonId = request.POST.get("exePythonId","")
    if not exePythonId:
        return HttpResponse(ApiReturn(ApiReturn.CODE_WARNING,message="exePythonId参数错误").toJson())
    try:
        exePythonData = TbExecPythonAttrs.objects.get(state=1, id=exePythonId)
    except Exception as e:
        return HttpResponse(ApiReturn(ApiReturn.CODE_WARNING,message="exePythonId查询错误 %s" % e).toJson())
    exePythonData.state = 0
    exePythonData.save()

    return HttpResponse(ApiReturn().toJson())

def resetExePython(request):
    exePythonId = request.POST.get("exePythonId","")
    if not exePythonId:
        return HttpResponse(ApiReturn(ApiReturn.CODE_WARNING,message="exePythonId参数错误").toJson())
    try:
        exePythonData = TbExecPythonAttrs.objects.get(state=0, id=exePythonId)
    except Exception as e:
        return HttpResponse(ApiReturn(ApiReturn.CODE_WARNING,message="exePythonId查询错误 %s" % e).toJson())
    exePythonData.state = 1
    exePythonData.save()

    return HttpResponse(ApiReturn().toJson())

def delRedisKey(request):
    redisKey = request.POST.get("key","")
    if redisKey == "":
        return HttpResponse(ApiReturn(ApiReturn.CODE_WARNING,message="必须有key参数！").toJson())
    try:
        RedisCache().del_data(redisKey)
    except Exception as e:
        return HttpResponse(ApiReturn(ApiReturn.CODE_WARNING,message="KEY[%s]查询错误 %s" % (redisKey,e)).toJson())
    return HttpResponse(ApiReturn().toJson())
