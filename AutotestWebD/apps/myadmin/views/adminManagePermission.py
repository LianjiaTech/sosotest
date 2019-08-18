from apps.myadmin.service.AdminManagePermissionService import AdminManagePermissionService
# Create your views here.
from urllib import parse

from apps.common.config import commonWebConfig
from apps.common.func.WebFunc import *

logger = logging.getLogger("django")

def permissionCheckPage(request):
    context = {}
    context["adminManagePermission_check"] = "active"
    return render(request, "myadmin/adminManagePermission/admin_adminManagePermission_check.html", context)

def getPermission(request):
    checkArr = json.loads(parse.unquote(request.POST.get("checkArr")))
    orderBy = request.POST.get("orderBy", "")
    page = request.POST.get("page")

    if isInt(page):
        page = int(page)
    else:
        addUserLog(request, "单接口管理->查看用例->获取数据->页面参数不合法", "FAIL")
        return HttpResponse("<script>alert('请验证页数参数');</script>")
    execSql = "SELECT t.* from tb_admin_manage_permission t WHERE 1=1 "
    checkList = []
    for key in checkArr:
        if checkArr[key] == "":
            continue
        checkList.append("%%%s%%" % checkArr[key])
        execSql += """ and t.%s """ % key
        execSql += """ LIKE %s"""
    execSql += """ ORDER BY %s""" % orderBy
    context = pagination(sqlStr=execSql,attrList=checkList,page=page,pageNum=commonWebConfig.userPageNum)

    response = render(request, "myadmin/adminManagePermission/subPages/adminManagePermission_sub_page.html",context)
    return response


def getPermissionForId(request):
    permissionId = request.POST.get("permissionId")
    try:
        permissionData = TbAdminManagePermission.objects.get(id=permissionId)
    except Exception as e:
        message = "权限查询出错 %s" % e
        logger.error(message)
        return HttpResponse(ApiReturn(code=ApiReturn.CODE_WARNING, message=message).toJson())
    return HttpResponse(ApiReturn(body=dbModelToDict(permissionData)).toJson())


def addPermission(request):
    permissionRequest = json.loads(request.POST.get("permissionData"))
    logger.info("addPermission %s" % request.POST.get("permissionData"))
    permissionKey = permissionRequest["permissionKey"]
    if permissionKey == "":
        return HttpResponse(
            ApiReturn(code=ApiReturn.CODE_WARNING, message="角色创建失败,请检查角色key不能为空").toJson())
    '''如果权限没有在权限表中添加过，那么新建，如果有添加过，那么判断是否有效'''
    searchResult = dbModelListToListDict(TbAdminManagePermission.objects.filter(permissionKey = permissionRequest["permissionKey"]))
    if permissionRequest["permissionValue"].startswith("/"):
        if len(searchResult) == 0:
            result = TbAdminManagePermission()
            result.permissionKey = permissionKey
            result.permissionName = permissionRequest["permissionName"]
            result.permissionValue = permissionRequest["permissionValue"]
            result.isDefaultPermission = permissionRequest["isDefaultPermission"]
            result.save()
            if result:
                logger.info("addPermission 角色创建成功 %s" % result)
            return HttpResponse(ApiReturn().toJson())
        else:

            searchResultDict = searchResult[0]
            if searchResultDict["state"] == 0:
                searchResultDict["state"] = 1
                searchResultDict["permissionName"] = permissionRequest["permissionName"]
                searchResultDict["permissionValue"] = permissionRequest["permissionValue"]
                searchResultDict["isDefaultPermission"] = permissionRequest["isDefaultPermission"]
                # PermissionService.updatePermission(searchResultDict)
                return HttpResponse(ApiReturn().toJson())
            else:
                logger.info("addPermission 权限创建失败")
                return HttpResponse(
                    ApiReturn(code=ApiReturn.CODE_WARNING, message="权限创建失败,请检查权限key是否重复").toJson())
    else:
        logger.info("addPermission 权限创建失败,permissionValue必须以/开头")
        return HttpResponse(ApiReturn(code=ApiReturn.CODE_WARNING, message="permissionValue必须以/开头").toJson())




def editPermission(request):
    try:
        requestDict =json.loads(request.POST.get("permissionData"))
        AdminManagePermissionService.updatePermission(requestDict)
    except Exception as e:
        print(traceback.format_exc())
        message = "编辑权限数据发生异常 %s" % e
        logger.info(message)
        return HttpResponse(ApiReturn(code=ApiReturn.CODE_WARNING, message=message).toJson())
    return HttpResponse(ApiReturn().toJson())

def delPermission(request):
    permissionId = request.POST.get("permissionId", "")
    if not permissionId:
        return HttpResponse(ApiReturn(ApiReturn.CODE_WARNING, message="permissionId参数错误").toJson())
    try:
        permissionData = TbAdminManagePermission.objects.get(state=1, id=permissionId)
    except Exception as e:
        return HttpResponse(ApiReturn(ApiReturn.CODE_WARNING, message="permissionId查询错误 %s" % e).toJson())
    permissionData.state = 0
    permissionData.save()
    '''删除权限后，删除关联关系'''
    TbAdminUserPermissionRelation.objects.filter(permissionKey=permissionData.permissionKey, state=1).update(state=0)
    TbAdminTeamPermissionRelation.objects.filter(permissionKey=permissionData.permissionKey, state=1).update(state=0)
    TbAdminRolePermissionRelation.objects.filter(permissionKey=permissionData.permissionKey, state=1).update(state=0)
    TbAdminInterfacePermissionRelation.objects.filter(permissionKey=permissionData.permissionKey, state=1).update(state=0)
    return HttpResponse(ApiReturn().toJson())

def resetPermission(request):
    permissionId = request.POST.get("permissionId", "")
    if not permissionId:
        return HttpResponse(ApiReturn(ApiReturn.CODE_WARNING, message="permissionId参数错误").toJson())
    try:
        permissionData = TbAdminManagePermission.objects.get(state=0, id=permissionId)
    except Exception as e:
        return HttpResponse(ApiReturn(ApiReturn.CODE_WARNING, message="permissionId查询错误 %s" % e).toJson())
    permissionData.state = 1
    permissionData.save()

    return HttpResponse(ApiReturn().toJson())



def getAllPermissions(request):
    try:
        permissionsResult = TbAdminManagePermission.objects.filter(state=1)
        permissionsDict = dbModelListToListDict(permissionsResult)
    except Exception as e:
        message = "查询权限出错 %s" % e
        logger.error(message)
        return HttpResponse(ApiReturn(code=ApiReturn.CODE_WARNING, message=message).toJson())
    return HttpResponse(ApiReturn(body=permissionsDict).toJson())


'''给单个用户授权时，获得所有选择的权限'''
def getAllSelectedPermissions(request):
    loginName = request.POST.get("loginName")
    usersPermissionResult = TbAdminManageUserPermissionRelation.objects.filter(state=1, loginName=loginName)
    if len(usersPermissionResult) == 0:
        return HttpResponse(ApiReturn().toJson())
    else:
        usersPermissionResultList = dbModelListToListDict(usersPermissionResult)
        list = []
        for userPermission in usersPermissionResultList:
            userPermissionDict = userPermission
            permissionKey = userPermissionDict["permissionKey"]
            permission = TbAdminManagePermission.objects.filter(permissionKey=permissionKey, state=1)
            usersListNew = dbModelListToListDict(permission)
            if len(usersListNew) != 0:
                list.append(usersListNew[0])
        return HttpResponse(ApiReturn(body=list).toJson())


'''给用户批量授权时，获得所有选择的权限'''
def getAllUsersSelectedPermissions(request):
    permissionResult = TbAdminManagePermission.objects.filter(state=1)
    if len(permissionResult) == 0:
        return HttpResponse(ApiReturn().toJson())
    else:
        permissionResultList = dbModelListToListDict(permissionResult)
        list = []
        for userPermission in permissionResultList:
            list.append(userPermission)
        return HttpResponse(ApiReturn(body=list).toJson())


'''给小组授权时，获得所有选择的权限'''
def getAllSelectedTeamPermissions(request):
    teamId = request.POST.get("teamId")
    teamResult = TbAdminTeam.objects.filter(id=teamId, state=1)
    teamList = dbModelListToListDict(teamResult)
    teamDict = teamList[0]
    teamKey = teamDict["teamKey"]
    teamPermissionResult = TbAdminTeamPermissionRelation.objects.filter(state=1, teamKey=teamKey)
    if len(teamPermissionResult) == 0:
        return HttpResponse(ApiReturn().toJson())
    else:
        teamPermissionResultList = dbModelListToListDict(teamPermissionResult)
        list = []
        for teamPermission in teamPermissionResultList:
            teamPermissionDict = teamPermission
            permissionKey = teamPermissionDict["permissionKey"]
            permission = TbAdminManagePermission.objects.filter(permissionKey=permissionKey)
            teamListNew = dbModelListToListDict(permission)
            if len(teamListNew) == 0:
                list = []
            else:
                list.append(teamListNew[0])
        return HttpResponse(ApiReturn(body=list).toJson())
