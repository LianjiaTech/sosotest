from urllib import parse

from apps.common.config import commonWebConfig
from apps.common.func.WebFunc import *
from apps.myadmin.service.InterfacePermissionService import InterfacePermissionService
from apps.common.model.RedisDBConfig import *
from apps.common.config.permissionConst import PermissionConst

logger = logging.getLogger("django")

def interfacePermissionCheckPage(request):
    context = {}
    context["interfacePermission_check"] = "active"
    return render(request, "myadmin/interfacePermission/admin_interfacePermission_check.html",context)

def getInterfacePermission(request):
    checkArr = json.loads(parse.unquote(request.POST.get("checkArr")))
    orderBy = request.POST.get("orderBy","")
    page = request.POST.get("page")
    if isInt(page):
        page = int(page)
    else:
        addUserLog(request, "单接口管理->查看用例->获取数据->页面参数不合法", "FAIL")
        return HttpResponse("<script>alert('请验证页数参数');</script>")
    execSql = "SELECT u.* from tb_admin_interface_permission_relation u WHERE 1=1 "
    checkList = []
    for key in checkArr:
        if checkArr[key] == "":
            continue
        checkList.append("%%%s%%" % checkArr[key])
        execSql += """ and u.%s """ % key
        execSql += """ LIKE %s"""
    execSql += """ ORDER BY %s""" % orderBy
    context = pagination(sqlStr=execSql,attrList=checkList,page=page,pageNum=commonWebConfig.userPageNum)
    for index in context["pageDatas"]:
        if index["isDefault"] == 1:
            index["isDefaultText"] = "是"
        else:
            index["isDefaultText"] = "否"
    response = render(request, "myadmin/interfacePermission/subPages/interfacePermission_sub_page.html",context)
    return response

def getInterfacePermissionForId(request):
    interfacePermissionId = request.POST.get("interfacePermissionId")
    try:
        interfacePermissionData = TbAdminInterfacePermissionRelation.objects.get(id=interfacePermissionId)
        requestDict = dbModelToDict(interfacePermissionData)
    except Exception as e:
        message = "查询接口权限出错 %s" % e
        logger.error(message)
        return HttpResponse(ApiReturn(code=ApiReturn.CODE_WARNING,message=message).toJson())
    return HttpResponse(ApiReturn(body=requestDict).toJson())


def addInterfacePermission(request):
    interfacePermissionRequest = json.loads(request.POST.get("interfacePermissionData"))
    logger.info("addInterfacePermission %s" % request.POST.get("interfacePermissionData"))
    interfacePermissionRequest["addTime"] = datetime.datetime.now()
    searchResult = TbAdminInterfacePermissionRelation.objects.filter(url=interfacePermissionRequest["url"], permissionKey=interfacePermissionRequest["permissionKey"])

    try:
        if len(searchResult) == 0:
            result = TbAdminInterfacePermissionRelation()
            result.url = interfacePermissionRequest["url"]
            result.permissionKey = interfacePermissionRequest["permissionKey"]
            result.save()
            if result:
                logger.info("addInterfacePermission 接口权限添加成功 %s" % result)
            return HttpResponse(ApiReturn().toJson())
        else:
            if searchResult.state == 0:
                searchResult.state = 1
                InterfacePermissionService.updateInterfacePermission(dbModelToDict(searchResult))
                return HttpResponse(ApiReturn().toJson())
            else:
                logger.info("addInterfacePermission 接口权限创建失败")
                return HttpResponse(ApiReturn(code=ApiReturn.CODE_WARNING, message="接口权限创建失败,请检查账号是否重复").toJson())
    except Exception as e:
        message = "添加接口权限失败 :%s" % e
        logger.info(message)
        return HttpResponse(ApiReturn(code=ApiReturn.CODE_WARNING, message="接口权限创建失败,请检查账号是否重复").toJson())


def editInterfacePermission(request):
    try:
        requestDict = json.loads(request.POST.get("interfacePermissionData"))

        try:
            RedisCache().del_data("%s_%s" % (PermissionConst.urlDefaultPermission,requestDict["url"]))
        except:
            pass

        requestDict["modTime"] = datetime.datetime.now()
        InterfacePermissionService.updateInterfacePermission(requestDict)

    except Exception as e:
        print(traceback.format_exc())
        message = "编辑接口权限发生异常 %s" % e
        logger.info(message)
        return HttpResponse(ApiReturn(code=ApiReturn.CODE_WARNING,message=message).toJson())

    return HttpResponse(ApiReturn().toJson())

def delInterfacePermission(request):
    interfacePermissionId = request.POST.get("interfacePermissionId","")
    if not interfacePermissionId:
        return HttpResponse(ApiReturn(ApiReturn.CODE_WARNING,message="interfacePermissionId参数错误").toJson())
    try:
        interfacePermissionData = TbAdminInterfacePermissionRelation.objects.get(state=1, id=interfacePermissionId)
    except Exception as e:
        return HttpResponse(ApiReturn(ApiReturn.CODE_WARNING,message="interfacePermissionId查询错误 %s" % e).toJson())
    interfacePermissionData.state = 0
    interfacePermissionData.save()

    return HttpResponse(ApiReturn().toJson())

def resetInterfacePermission(request):
    interfacePermissionId = request.POST.get("interfacePermissionId","")
    if not interfacePermissionId:
        return HttpResponse(ApiReturn(ApiReturn.CODE_WARNING,message="interfacePermissionId参数错误").toJson())
    try:
        interfacePermissionData = TbAdminInterfacePermissionRelation.objects.get(state=0, id=interfacePermissionId)
    except Exception as e:
        return HttpResponse(ApiReturn(ApiReturn.CODE_WARNING,message="interfacePermissionId查询错误 %s" % e).toJson())
    interfacePermissionData.state = 1
    interfacePermissionData.save()

    return HttpResponse(ApiReturn().toJson())

# def getAllInterface(request):
#     interfaceList = TbAdminInterfaceModuleRelation.objects.filter(state=1)
#     urlList = []
#     if len(interfaceList) == 0:
#         return HttpResponse(ApiReturn(code=ApiReturn.CODE_WARNING, message="没有可用接口,请联系管理员").toJson())
#     for interfaceIndex in interfaceList:
#         if interfaceIndex.url not in urlList:
#             urlList.append(interfaceIndex.url)
#     return HttpResponse(ApiReturn(body=urlList).toJson())

def getAllPermissionKeys(request):
    permissionsList = TbAdminInterfacePermissionRelation.objects.filter(state=1)
    permissionKeysList = []
    if len(permissionsList) == 0:
        return HttpResponse(ApiReturn(code=ApiReturn.CODE_WARNING, message="没有可用权限，请联系管理员").toJson())
    for permissionIndex in permissionsList:
        tmpDict = {}
        tmpDict["permissionKey"] = permissionIndex.permissionKey
        tmpDict["permissionName"] = permissionIndex.permissionName
        permissionKeysList.append(tmpDict)
    return HttpResponse(ApiReturn(body=permissionKeysList).toJson())
