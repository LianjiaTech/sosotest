from urllib import parse

# Create your views here.
from apps.common.config import commonWebConfig
from apps.common.func.WebFunc import *
from apps.myadmin.service.AdminManageUserPermissionRelationService import AdminManageUserPermissionRelationService
from apps.myadmin.service.AdminUserService import AdminUserService

logger = logging.getLogger("django")

def adminUserCheckPage(request):
    context = {}
    context["adminUser_check"] = "active"
    return render(request,"myadmin/adminUser/admin_adminUser_check.html",context)

def getAdminUser(request):
    checkArr = json.loads(parse.unquote(request.POST.get("checkArr")))
    orderBy = request.POST.get("orderBy","")
    page = request.POST.get("page")
    if isInt(page):
        page = int(page)
    else:
        addUserLog(request, "单接口管理->查看用例->获取数据->页面参数不合法", "FAIL")
        return HttpResponse("<script>alert('请验证页数参数');</script>")
    execSql = "SELECT u.* from tb_admin_user u WHERE 1=1 "
    checkList = []
    for key in checkArr:
        if checkArr[key] == "":
            continue
        checkList.append("%%%s%%" % checkArr[key])
        execSql += """ and u.%s """ % key
        execSql += """ LIKE %s"""
    execSql += """ ORDER BY %s""" % orderBy
    context = pagination(sqlStr=execSql,attrList=checkList,page=page,pageNum=commonWebConfig.userPageNum)
    response = render(request, "myadmin/adminUser/subPages/adminUser_sub_page.html",context)
    return response

def getAdminUserForId(request):
    userId = request.POST.get("userId")
    try:
        userData = TbAdminUser.objects.get(id=userId)
        requestDict = dbModelToDict(userData)
        del requestDict["passWord"]
    except Exception as e:
        message = "查询用户出错 %s" % e
        logger.error(message)
        return HttpResponse(ApiReturn(code=ApiReturn.CODE_WARNING,message=message).toJson())
    return HttpResponse(ApiReturn(body=requestDict).toJson())


def addAdminUser(request):
    userRequest = json.loads(request.POST.get("userData"))
    logger.info("addUser %s" % request.POST.get("userData"))
    if userRequest["passWord"] != userRequest["passWord1"]:
        return HttpResponse(ApiReturn(code=ApiReturn.CODE_ERROR, message="两次密码输入不一致,请检查重新输入").toJson())
    del userRequest["passWord1"]
    pwdMd5 = hashlib.md5()
    pwdMd5.update(userRequest["passWord"].encode("utf-8"))
    userRequest["passWord"] = pwdMd5.hexdigest()
    searchResult = TbAdminUser.objects.filter(loginName=userRequest["loginName"])
    searchResultList = dbModelListToListDict(searchResult)
    try:
        if len(searchResultList) == 0:
            result = TbAdminUser()
            result.loginName = userRequest["loginName"]
            result.userName = userRequest["userName"]
            result.superManager = userRequest["superManager"]
            result.email = userRequest["email"]
            result.passWord = userRequest["passWord"]
            result.save()

            # if userRequest["superManager"] == "1":
            #     AdminUserService.addAllPermissions(userRequest["loginName"])
            # else:
            #     AdminUserService.addDefaultPermission(userRequest["loginName"])
            if result:
                logger.info("addAdminUser 管理员添加成功 %s" % result)
            return HttpResponse(ApiReturn().toJson())
        else:
            searchResultDict = searchResultList[0]
            if searchResultDict["state"] == 0:
                #如果新建的管理员名称和已经删除的管理员名称一样，进行更新数据
                if searchResultDict["userName"] == userRequest["userName"]:
                    searchResultDict["state"] = 1
                    AdminUserService.updateAdminUser(searchResultDict)
                    if searchResultDict["superManager"] == 1:
                        return HttpResponse(ApiReturn().toJson())
                        # AdminUserService.addAllPermissions(userRequest["loginName"])
                    # else:
                    #     AdminUserService.addDefaultPermission(userRequest["loginName"])
                    return HttpResponse(ApiReturn().toJson())
                else:
                    logger.info("addAdminUser 管理员创建失败")
                    return HttpResponse(ApiReturn(code=ApiReturn.CODE_WARNING, message="管理员创建失败,请检查账号是否重复").toJson())
            else:
                logger.info("addAdminUser 管理员创建失败")
                return HttpResponse(ApiReturn(code=ApiReturn.CODE_WARNING, message="管理员创建失败,请检查账号是否重复").toJson())
    except Exception as e:
        message = "添加管理员失败 :%s" % e
        logger.info(message)
        return HttpResponse(ApiReturn(code=ApiReturn.CODE_WARNING, message="管理员创建失败,请检查账号是否重复").toJson())


def editAdminUser(request):
    try:
        requestDict = json.loads(request.POST.get("userData"))
        if requestDict["passWord"] != requestDict["passWord1"]:
            return HttpResponse(ApiReturn(code=ApiReturn.CODE_ERROR,message="两次密码输入不一致,请检查重新输入" ).toJson())
        '''如果没有填写密码，就使用默认密码'''
        if requestDict["passWord"] == "" and requestDict["passWord1"] == "":
            del requestDict["passWord1"]
            pwdMd5 = hashlib.md5()
            pwdMd5.update("123456".encode("utf-8"))
            requestDict["passWord"] = pwdMd5.hexdigest()
            AdminUserService.updateAdminUser(requestDict)
            return HttpResponse(ApiReturn().toJson())
        del requestDict["passWord1"]
        pwdMd5 = hashlib.md5()
        pwdMd5.update(requestDict["passWord"].encode("utf-8"))
        requestDict["passWord"] = pwdMd5.hexdigest()
        requestDict["modTime"] = datetime.datetime.now()
        AdminUserService.updateAdminUser(requestDict)

    except Exception as e:
        print(traceback.format_exc())
        message = "编辑用户数据发生异常 %s" % e
        logger.info(message)
        return HttpResponse(ApiReturn(code=ApiReturn.CODE_WARNING,message=message).toJson())

    return HttpResponse(ApiReturn().toJson())

def delAdminUser(request):
    userId = request.POST.get("userId","")
    if not userId:
        return HttpResponse(ApiReturn(ApiReturn.CODE_WARNING,message="userId参数错误").toJson())
    try:
        userData = TbAdminUser.objects.get(state=1, id=userId)
    except Exception as e:
        return HttpResponse(ApiReturn(ApiReturn.CODE_WARNING,message="userId查询错误 %s" % e).toJson())
    userData.state = 0
    userData.save()
    '''删除user时，删除关联关系'''
    TbAdminPlatformPermissionUserRelation.objects.filter(loginName=userData.loginName, state=1).update(state=0)
    TbAdminManageUserPermissionRelation.objects.filter(loginName=userData.loginName, state=1).update(state=0)
    TbAdminUserRoleRelation.objects.filter(loginName=userData.loginName, state=1).update(state=0)

    return HttpResponse(ApiReturn().toJson())

def resetAdminUser(request):
    userId = request.POST.get("userId","")
    if not userId:
        return HttpResponse(ApiReturn(ApiReturn.CODE_WARNING,message="userId参数错误").toJson())
    try:
        userData = TbAdminUser.objects.get(state=0, id=userId)
    except Exception as e:
        return HttpResponse(ApiReturn(ApiReturn.CODE_WARNING,message="userId查询错误 %s" % e).toJson())
    userData.state = 1
    userData.save()
    # AdminUserService.addDefaultPermission(userData.loginName)

    return HttpResponse(ApiReturn().toJson())


'''给单个用户授权'''
def addPermissionsToUser(request):
    userRequest = json.loads(request.POST.get("userPermissionsData"))
    print(userRequest)
    logger.info("addPermission %s" % request.POST.get("userPermissionsData"))
    loginName = userRequest["loginName"]
    permissionKeys = userRequest["permissionKeys"]
    userPermissionsData = {}
    relationData = TbAdminManageUserPermissionRelation.objects.filter(loginName=loginName)
    relationDataList = dbModelListToListDict(relationData)
    for relation in relationDataList:
        '''判断loginName已经插入到数据库中的权限，是否在这次需要插入的permission列表中'''
        relationPermissionKey = relation["permissionKey"]
        '''如果在列表中，说明该permission是这次需要增加的；并且state=0，那么需要更新'''
        if relationPermissionKey in permissionKeys:
            if relation["state"] == 0:
                relation["state"] =1
                AdminManageUserPermissionRelationService.updateUserPermission(relation)
        else:
            '''如果不在列表中，说明该permission是这次需要删除的；并且state=1，将state置为0'''
            if relation["state"] == 1:
                relation["state"] = 0
                AdminManageUserPermissionRelationService.updateUserPermission(relation)

    '''判断loginName是否已经有授权permissionKey,如果没有授权，新增；如果有授权，判断该授权是否已经删除，如果已经删除了，进行更新'''
    for permissionKey in permissionKeys:
        userPermissionsData["loginName"] = loginName
        userPermissionsData["permissionKey"] = permissionKey
        data = TbAdminManageUserPermissionRelation.objects.filter(loginName=loginName, permissionKey=permissionKey)
        '''没有授权，新增'''
        if len(data) == 0:
            result = TbAdminManageUserPermissionRelation()
            result.loginName = userPermissionsData["loginName"]
            result.permissionKey = userPermissionsData["permissionKey"]
            result.save()
        else:
            '''有授权，判断授权是否被删除了'''
            permissionList = dbModelListToListDict(data)
            for permissionIndex in permissionList:
                if permissionIndex["state"] == 0:
                    AdminManageUserPermissionRelationService.updateUserPermission(userPermissionsData)
    return HttpResponse(ApiReturn().toJson())


