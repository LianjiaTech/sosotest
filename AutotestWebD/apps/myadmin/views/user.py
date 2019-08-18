from urllib import parse

# Create your views here.
from apps.common.config import commonWebConfig
from apps.common.config import permissionConst
from apps.common.func.WebFunc import *
from apps.myadmin.service.UserPermissionRelationService import UserPermissionRelationService
from apps.myadmin.service.UserService import UserService
from apps.common.model.RedisDBConfig import RedisCache
from apps.common.config.permissionConst import PermissionConst
from django.db.models import Q

logger = logging.getLogger("django")

def userCheckPage(request):
    context = {}
    context["user_check"] = "active"
    return render(request,"myadmin/user/admin_user_check.html",context)

def getUser(request):
    checkArr = json.loads(parse.unquote(request.POST.get("checkArr")))
    orderBy = request.POST.get("orderBy","")
    page = request.POST.get("page")
    if isInt(page):
        page = int(page)
    else:
        addUserLog(request, "单接口管理->查看用例->获取数据->页面参数不合法", "FAIL")
        return HttpResponse("<script>alert('请验证页数参数');</script>")
    execSql = "SELECT u.* from tb_user u WHERE 1=1  "
    checkList = []
    for key in checkArr:
        if checkArr[key] == "":
            continue
        checkList.append("%%%s%%" % checkArr[key])
        execSql += """ and u.%s """ % key
        execSql += """ LIKE %s"""
    execSql += """ ORDER BY %s,u.state asc""" % orderBy
    context = pagination(sqlStr=execSql,attrList=checkList,page=page,pageNum=commonWebConfig.userPageNum)
    for userIndex in context["pageDatas"]:
        userIndex["typeText"] = "未选择"
        if userIndex["type"] == 1:
            userIndex["typeText"] = "开发人员"
        elif userIndex["type"] == 2:
            userIndex["typeText"] = "测试人员"

        userIndex["auditText"] = "0未审核 1审核中 2通过 3未通过"
        if userIndex["audit"] == 1:
            userIndex["auditText"] = "审核中"
        elif userIndex["audit"] == 2:
            userIndex["auditText"] = "通过"
        else:
            userIndex["auditText"] = "未通过"

        if userIndex["token"] == None or userIndex["token"] == "":
            userIndex["token"] = "无"

    response = render(request, "myadmin/user/subPages/user_sub_page.html",context)
    return response



def getUserForId(request):
    userId = request.POST.get("userId")
    try:
        userData = TbUser.objects.get(id=userId)
        requestDict = dbModelToDict(userData)
        del requestDict["pwd"]
    except Exception as e:
        message = "查询用户出错 %s" % e
        logger.error(message)
        return HttpResponse(ApiReturn(code=ApiReturn.CODE_WARNING,message=message).toJson())
    return HttpResponse(ApiReturn(body=requestDict).toJson())




def addUser(request):
    userRequest = json.loads(request.POST.get("userData"))
    logger.info("addUser %s" % request.POST.get("userData"))
    if userRequest["pwd"] != userRequest["pwd1"]:
        return HttpResponse(ApiReturn(code=ApiReturn.CODE_ERROR, message="两次密码输入不一致,请检查重新输入").toJson())
    del userRequest["pwd1"]
    pwdMd5 = hashlib.md5()
    pwdMd5.update(userRequest["pwd"].encode("utf-8"))
    userRequest["pwd"] = pwdMd5.hexdigest()
    userRequest["addTime"] = datetime.datetime.now()
    searchResult = TbUser.objects.filter(loginName=userRequest["loginName"])
    searchResultList = dbModelListToListDict(searchResult)
    try:
        '''没有loginName在user中,新建user，并授权'''
        if len(searchResultList) == 0:
            if userRequest["token"] != "" and len(TbUser.objects.filter(token=userRequest["token"])) > 0:
                return HttpResponse(ApiReturn(code=ApiReturn.CODE_WARNING, message="用户创建失败,请检查token是否重复").toJson())
            result = TbUser()
            result.loginName = userRequest["loginName"]
            result.userName = userRequest["userName"]
            result.token = userRequest["token"]
            result.email = userRequest["email"]
            result.addTime = userRequest["addTime"]
            result.pwd = userRequest["pwd"]
            result.audit = userRequest["audit"]
            result.type = userRequest["type"]
            result.state = userRequest["state"]
            result.defaultPermission = userRequest["defaultPermission"]
            result.save()
            if result:
                logger.info("addUser 用户创建成功 %s" % result)
            return HttpResponse(ApiReturn().toJson())
        else:
            if userRequest["token"] != "" and len(TbUser.objects.filter(token=userRequest["token"],state=1)) > 0:
                return HttpResponse(ApiReturn(code=ApiReturn.CODE_WARNING, message="用户创建失败,请检查token是否重复").toJson())
            '''loginName已经被删除了,更新user，并授权'''
            searchResultDict = searchResultList[0]
            if searchResultDict["state"] == 0:
                searchResultDict["state"] = 1
                searchResultDict["userName"] = userRequest["userName"]
                searchResultDict["pwd"] = userRequest["pwd"]
                searchResultDict["token"] = userRequest["token"]
                searchResultDict["email"] = userRequest["email"]
                searchResultDict["audit"] = userRequest["audit"]
                searchResultDict["type"] = userRequest["type"]
                searchResultDict["state"] = userRequest["state"]
                searchResultDict["defaultPermission"] = userRequest["defaultPermission"]
                UserService.updateUser(searchResultDict)
                return HttpResponse(ApiReturn().toJson())
            else:
                logger.info("addUser 用户创建失败")
                return HttpResponse(ApiReturn(code=ApiReturn.CODE_WARNING, message="用户创建失败,请检查账号是否重复").toJson())
    except Exception as e:
        message = "添加用户发生异常： %s" % e
        logger.info(message)
        return HttpResponse(ApiReturn(code=ApiReturn.CODE_WARNING, message="用户创建失败,请检查账号是否重复").toJson())


def editUser(request):
    try:
        requestDict = json.loads(request.POST.get("userData"))
        try:
            RedisCache().del_data("%s_%s" % (PermissionConst.user_permission,requestDict["loginName"]))
        except:
            pass

        if requestDict["pwd"] != requestDict["pwd1"]:
            return HttpResponse(ApiReturn(code=ApiReturn.CODE_ERROR,message="两次密码输入不一致,请检查重新输入" ).toJson())
        if requestDict["token"] != "" and len(TbUser.objects.filter(token=requestDict["token"], state=1,).filter(~Q(loginName=requestDict["loginName"]))) > 0:
            return HttpResponse(ApiReturn(code=ApiReturn.CODE_WARNING, message="用户创建失败,请检查token是否重复").toJson())
        '''如果编辑时，用户没有输入密码，那么就给密码赋值默认值'''
        if requestDict["pwd"] == "" and requestDict["pwd1"] == "":
            del requestDict["pwd1"]
            pwdMd5 = hashlib.md5()
            pwdMd5.update("123456".encode("utf-8"))
            requestDict["pwd"] = pwdMd5.hexdigest()
            UserService.updateUser(requestDict)
            return HttpResponse(ApiReturn().toJson())
        del requestDict["pwd1"]
        pwdMd5 = hashlib.md5()
        pwdMd5.update(requestDict["pwd"].encode("utf-8"))
        requestDict["pwd"] = pwdMd5.hexdigest()
        UserService.updateUser(requestDict)

    except Exception as e:
        print(traceback.format_exc())
        message = "编辑用户数据发生异常 %s" % e
        logger.info(message)
        return HttpResponse(ApiReturn(code=ApiReturn.CODE_WARNING,message=message).toJson())

    return HttpResponse(ApiReturn().toJson())



def delUser(request):
    userId = request.POST.get("userId","")
    if not userId:
        return HttpResponse(ApiReturn(ApiReturn.CODE_WARNING,message="userId参数错误").toJson())
    try:
        userData = TbUser.objects.get(state=1,id=userId)
    except Exception as e:
        return HttpResponse(ApiReturn(ApiReturn.CODE_WARNING,message="userId查询错误 %s" % e).toJson())
    userData.state = 0
    userData.save()
    '''删除user时，删除关联关系'''
    TbUserPermissionRelation.objects.filter(loginName=userData.loginName, state=1).update(state=0)
    TbAdminUserTeamRelation.objects.filter(loginName=userData.loginName, state=1).update(state=0)
    TbAdminUserRoleRelation.objects.filter(loginName=userData.loginName, state=1).update(state=0)


    return HttpResponse(ApiReturn().toJson())

'''给单个用户授权'''
def addPermissionsToUser(request):
    userRequest = json.loads(request.POST.get("userPermissionsData"))
    logger.info("addPermission %s" % request.POST.get("userPermissionsData"))
    loginName = userRequest["loginName"]
    try:
        RedisCache().del_data("%s_%s"%(PermissionConst.user_permission,loginName))
    except:
        pass
    # loginName = dbModelListToListDict(TbUser.objects.filter(id=userId))[0]["loginName"]
    permissionKeys = userRequest["permissionKeys"]
    userPermissionsData = {}
    # relationData = TbAdminUserPermissionRelation.objects.filter(loginName=loginName)
    relationData = TbUserPermissionRelation.objects.filter(loginName=loginName)
    relationDataList = dbModelListToListDict(relationData)
    for relation in relationDataList:
        '''判断loginName已经插入到数据库中的权限，是否在这次需要插入的permission列表中'''
        relationPermissionKey = relation["permissionKey"]
        '''如果在列表中，说明该permission是这次需要增加的；并且state=0，那么需要更新'''
        if relationPermissionKey in permissionKeys:
            if relation["state"] == 0:
                relation["state"] =1
                UserPermissionRelationService.updateUserPermission(relation)
        else:
            '''如果不在列表中，说明该permission是这次需要删除的；并且state=1，将state置为0'''
            if relation["state"] == 1:
                relation["state"] = 0
                UserPermissionRelationService.updateUserPermission(relation)

    '''判断loginName是否已经有授权permissionKey,如果没有授权，新增；如果有授权，判断该授权是否已经删除，如果已经删除了，进行更新'''
    for permissionKey in permissionKeys:
        userPermissionsData["loginName"] = loginName
        userPermissionsData["permissionKey"] = permissionKey
        data = TbUserPermissionRelation.objects.filter(loginName=loginName, permissionKey=permissionKey)
        '''没有授权，新增'''
        if len(data) == 0:
            result = TbUserPermissionRelation()
            result.loginName = userPermissionsData["loginName"]
            result.permissionKey = userPermissionsData["permissionKey"]
            result.save()
        else:
            '''有授权，判断授权是否被删除了'''
            permissionList = dbModelListToListDict(data)
            for permissionIndex in permissionList:
                if permissionIndex["state"] == 0:
                    UserPermissionRelationService.updateUserPermission(userPermissionsData)
    return HttpResponse(ApiReturn().toJson())

'''给所有用户授权'''
def addPermissionsToAllUsers(request):
    userRequest = json.loads(request.POST.get("userPermissionsData"))
    logger.info("addPermission %s" % request.POST.get("userPermissionsData"))

    userList = TbUser.objects.filter(state=1)
    for userIndex in userList:
        loginName = userIndex.loginName
        permissionKeys = userRequest["permissionKeys"]
        userPermissionsData = {}
        relationDataList = TbUserPermissionRelation.objects.filter(loginName=loginName)
        for relation in relationDataList:
            relationPermissionKey = relation.permissionKey
            if relationPermissionKey in permissionKeys:
                if relation.state == 0:
                    relation.state = 1
                    relation.save()
            else:
                if relation.state == 1:
                    relation.state = 0
                    relation.save()

        for permissionKey in permissionKeys:
            userPermissionsData["loginName"] = loginName
            userPermissionsData["permissionKey"] = permissionKey
            data = TbAdminUserPermissionRelation.objects.filter(loginName=loginName, permissionKey=permissionKey)
            if len(data) == 0:
                result = TbAdminUserPermissionRelation()
                result.loginName = userPermissionsData["loginName"]
                result.permissionKey = userPermissionsData["permissionKey"]
                result.save()
            else:
                permission = data
                for user in permission:
                    if user.state == 0:
                        user.save()

    return HttpResponse(ApiReturn().toJson())

def getUserPermission(request):
    loginName = request.POST.get("loginName")
    permission = TbUserPermissionRelation.objects.filter(loginName=loginName,state=1)
    permissionList = []
    for index in permission:
        tmpDict = {}
        tmpDict["permissionKey"] = index.permissionKey
        try:
            tmpDict["permissionName"] = TbAdminInterfacePermissionRelation.objects.get(permissionKey=index.permissionKey).permissionName
        except:
            tmpDict["permissionName"] = ""
        permissionList.append(tmpDict)
    return HttpResponse(ApiReturn(body=permissionList).toJson())



