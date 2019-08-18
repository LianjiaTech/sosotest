from urllib import parse

# Create your views here.
from all_models.models import TbAdminRole, TbAdminUserRoleRelation, TbAdminRolePermissionRelation
from apps.common.config import commonWebConfig
from apps.common.func.WebFunc import *
from apps.myadmin.service.RoleService import RoleService

logger = logging.getLogger("django")

def roleCheckPage(request):
    context = {}
    context["role_check"] = "active"
    return render(request, "myadmin/role/admin_role_check.html", context)

def getRole(request):
    checkArr = json.loads(parse.unquote(request.POST.get("checkArr")))
    orderBy = request.POST.get("orderBy", "")
    page = request.POST.get("page")

    if isInt(page):
        page = int(page)
    else:
        addUserLog(request, "单接口管理->查看用例->获取数据->页面参数不合法", "FAIL")
        return HttpResponse("<script>alert('请验证页数参数');</script>")
    execSql = "SELECT t.* from tb_admin_role t WHERE 1=1  "
    checkList = []
    for key in checkArr:
        if checkArr[key] == "":
            continue
        checkList.append("%%%s%%" % checkArr[key])
        execSql += """ and t.%s """ % key
        execSql += """ LIKE %s"""
    execSql += """ ORDER BY %s""" % orderBy
    context = pagination(sqlStr=execSql,attrList=checkList,page=page,pageNum=commonWebConfig.userPageNum)

    response = render(request, "myadmin/role/subPages/role_sub_page.html",context)
    return response


def getRoleForId(request):
    roleId = request.POST.get("roleId")
    try:
        roleData = TbAdminRole.objects.get(id=roleId)
    except Exception as e:
        message = "小组查询出错 %s" % e
        logger.error(message)
        return HttpResponse(ApiReturn(code=ApiReturn.CODE_WARNING,message=message).toJson())
    print(dbModelToDict(roleData))
    return HttpResponse(ApiReturn(body=dbModelToDict(roleData)).toJson())

def addRole(request):
    roleRequest = json.loads(request.POST.get("roleData"))
    logger.info("addRole %s" % request.POST.get("roleData"))
    roleRequest["addTime"] = datetime.datetime.now()
    searchResult = dbModelListToListDict(TbAdminRole.objects.filter(roleKey = roleRequest["roleKey"]))
    if len(searchResult) == 0:
        result = TbAdminRole()
        result.roleKey = roleRequest["roleKey"]
        result.roleName = roleRequest["roleName"]
        result.addTime = roleRequest["addTime"]
        result.save()
        if result:
            logger.info("addRole 角色创建成功 %s" % result)
        return HttpResponse(ApiReturn().toJson())
    else:

        searchResultDict = searchResult[0]
        if searchResultDict["state"] == 0:
            searchResultDict["state"] = 1
            searchResultDict["roleName"] = roleRequest["roleName"]
            RoleService.updateRole(searchResultDict)
            return HttpResponse(ApiReturn().toJson())
        else:
            logger.info("addRole 角色创建失败")
            return HttpResponse(
                ApiReturn(code=ApiReturn.CODE_WARNING, message="角色创建失败,请检查角色key是否重复").toJson())

    return HttpResponse(ApiReturn().toJson())


def editRole(request):
    try:
        requestDict =json.loads(request.POST.get("roleData"))
        requestDict["modTime"] = datetime.datetime.now()
        RoleService.updateRole(requestDict)
    except Exception as e:
        print(traceback.format_exc())
        message = "编辑角色数据发生异常 %s" % e
        logger.info(message)
        return HttpResponse(ApiReturn(code=ApiReturn.CODE_WARNING, message=message).toJson())

    return HttpResponse(ApiReturn().toJson())

def delRole(request):
    roleId = request.POST.get("roleId", "")
    if not roleId:
        return HttpResponse(ApiReturn(ApiReturn.CODE_WARNING, message="roleId参数错误").toJson())
    try:
        roleData = TbAdminRole.objects.get(state=1, id=roleId)
    except Exception as e:
        return HttpResponse(ApiReturn(ApiReturn.CODE_WARNING, message="roleId查询错误 %s" % e).toJson())
    roleData.state = 0
    roleData.save()
    TbAdminUserRoleRelation.objects.filter(roleKey=roleData.roleKey, state=1).update(state=0)
    TbAdminRolePermissionRelation.objects.filter(roleKey=roleData.roleKey, state=1).update(state=0)

    return HttpResponse(ApiReturn().toJson())

def resetRole(request):
    roleId = request.POST.get("roleId", "")
    if not roleId:
        return HttpResponse(ApiReturn(ApiReturn.CODE_WARNING, message="roleId参数错误").toJson())
    try:
        roleData = TbAdminRole.objects.get(state=0, id=roleId)
    except Exception as e:
        return HttpResponse(ApiReturn(ApiReturn.CODE_WARNING, message="roleId查询错误 %s" % e).toJson())
    roleData.state = 1
    roleData.save()


    return HttpResponse(ApiReturn().toJson())

def addUsersToRole(request):

    roleRequest = json.loads(request.POST.get("teamData"))
    logger.info("addTeam %s" % request.POST.get("teamData"))
    roleRequest["addTime"] = datetime.datetime.now()

    try:
        try:
            searchResult = TbAdminRole.objects.get(teamName=roleRequest["roleName"])
            searchResultDict = dbModelToDict(searchResult)
            if searchResult:
                if searchResultDict["state"] == 0:
                    searchResultDict["state"] = 1
                    RoleService.updateRole(searchResultDict)
                else:
                    logger.info("addTeam 小组创建失败")
                    return HttpResponse(
                        ApiReturn(code=ApiReturn.CODE_WARNING, message="小组创建失败,请检查小组名称是否重复").toJson())
        except:
            result = TbAdminRole.objects.create(**roleRequest)
            if result:
                logger.info("addTeam 小组创建成功 %s" % result)
    except Exception as e:
        logger.info("addTeam 小组创建失败 %s" % e)
        return HttpResponse(ApiReturn(code=ApiReturn.CODE_WARNING, message="小组创建失败 %s,请检查小组名称是否重复" % e).toJson())
    return HttpResponse(ApiReturn().toJson())