from urllib import parse

# Create your views here.
from all_models.models import *
from apps.common.config import commonWebConfig
from apps.common.func.WebFunc import *
# from apps.myadmin.service.InterfaceModuleService import InterfaceModuleService
from apps.myadmin.service.InterfacePermissionService import InterfacePermissionService
from apps.myadmin.service.ModuleService import ModuleService
from apps.myadmin.service.UserPermissionRelationService import UserPermissionRelationService
from apps.myadmin.service.UserService import UserService

logger = logging.getLogger("django")

def moduleManageCheckPage(request):
    context = {}
    context["moduleManage_check"] = "active"
    return render(request, "myadmin/moduleManage/admin_moduleManage_check.html",context)

def getModuleManage(request):
    checkArr = json.loads(parse.unquote(request.POST.get("checkArr")))
    orderBy = request.POST.get("orderBy","")
    page = request.POST.get("page")
    if isInt(page):
        page = int(page)
    else:
        return HttpResponse("<script>alert('请验证页数参数');</script>")
    execSql = "SELECT u.* from tb_modules u WHERE 1=1 "
    checkList = []
    for key in checkArr:
        if checkArr[key] == "":
            continue
        checkList.append("%%%s%%" % checkArr[key])
        execSql += """ and u.%s """ % key
        execSql += """ LIKE %s"""
    execSql += """ ORDER BY %s""" % orderBy
    context = pagination(sqlStr=execSql,attrList=checkList,page=page,pageNum=commonWebConfig.userPageNum)
    print("context::::::",context)
    response = render(request, "myadmin/moduleManage/subPages/moduleManage_sub_page.html",context)
    return response

def getModuleManageForId(request):
    moduleId = request.POST.get("moduleId")
    try:
        moduleData = TbModules.objects.get(id=moduleId)
        requestDict = dbModelToDict(moduleData)
    except Exception as e:
        message = "查询模块出错 %s" % e
        logger.error(message)
        return HttpResponse(ApiReturn(code=ApiReturn.CODE_WARNING,message=message).toJson())
    return HttpResponse(ApiReturn(body=requestDict).toJson())


def addModuleManage(request):
    moduleRequest = json.loads(request.POST.get("moduleManageData"))
    logger.info("addInterfacePermission %s" % request.POST.get("interfacePermissionData"))
    moduleRequest["addTime"] = datetime.datetime.now()
    searchResult = dbModelListToListDict(TbModules.objects.filter(moduleName=moduleRequest["moduleName"]))

    try:
        if len(searchResult) == 0:
            result = TbModules()
            result.moduleName = moduleRequest["moduleName"]
            result.moduleDesc = moduleRequest["moduleDesc"]
            result.save()
            if result:
                logger.info("addModuleManage 模块添加成功 %s" % result)
            return HttpResponse(ApiReturn().toJson())
        else:
            searchData = searchResult[0]
            if searchData["state"] == 0:
                searchData["state"] = 1
                searchData["moduleDesc"] = moduleRequest["moduleDesc"]
                ModuleService.updateModule(searchData)
                return HttpResponse(ApiReturn().toJson())
            else:
                logger.info("addModuleManage 模块创建失败")
                return HttpResponse(ApiReturn(code=ApiReturn.CODE_WARNING, message="模块创建失败,请检查账号是否重复").toJson())
    except Exception as e:
        message = "添加模块失败 :%s" % e
        logger.info(message)
        return HttpResponse(ApiReturn(code=ApiReturn.CODE_WARNING, message="模块创建失败,请检查账号是否重复").toJson())


def editModuleManage(request):
    try:
        requestDict = json.loads(request.POST.get("moduleManageData"))
        requestDict["modTime"] = datetime.datetime.now()
        ModuleService.updateModule(requestDict)

    except Exception as e:
        print(traceback.format_exc())
        message = "编辑模块发生异常 %s" % e
        logger.info(message)
        return HttpResponse(ApiReturn(code=ApiReturn.CODE_WARNING,message=message).toJson())

    return HttpResponse(ApiReturn().toJson())

def delModuleManage(request):
    moduleId = request.POST.get("moduleId","")
    if not moduleId:
        return HttpResponse(ApiReturn(ApiReturn.CODE_WARNING,message="moduleId参数错误").toJson())
    try:
        moduleData = TbModules.objects.get(state=1, id=moduleId)
    except Exception as e:
        return HttpResponse(ApiReturn(ApiReturn.CODE_WARNING,message="moduleId查询错误 %s" % e).toJson())
    moduleData.state = 0
    moduleData.save()

    return HttpResponse(ApiReturn().toJson())

def resetModuleManage(request):
    moduleId = request.POST.get("moduleId","")
    if not moduleId:
        return HttpResponse(ApiReturn(ApiReturn.CODE_WARNING,message="moduleId参数错误").toJson())
    try:
        moduleData = TbModules.objects.get(state=0, id=moduleId)
    except Exception as e:
        return HttpResponse(ApiReturn(ApiReturn.CODE_WARNING,message="moduleId查询错误 %s" % e).toJson())
    moduleData.state = 1
    moduleData.save()

    return HttpResponse(ApiReturn().toJson())

