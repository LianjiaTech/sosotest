# Create your views here.
import json
from urllib import parse

from all_models.models import *
from apps.common.config import commonWebConfig
from apps.common.func.WebFunc import *
from apps.myadmin.service.AdminUserService import AdminUserService
from apps.myadmin.service.PlatformPermissionUserService import PlatformPermissionUserService
from apps.myadmin.service.UserRoleRelationService import UserRoleRelationService


logger = logging.getLogger("django")

def userRoleCheckPage(request):
    context = {}
    context["userRole_check"] = "active"
    return render(request, "myadmin/userRole/admin_user_role_check.html", context)

def getUserRole(request):
    checkArr = json.loads(parse.unquote(request.POST.get("checkArr")))
    orderBy = request.POST.get("orderBy","")
    page = request.POST.get("page")
    teamId = request.POST.get("teamId")
    teamResult = TbAdminTeam.objects.filter(id=teamId)
    teamList = dbModelListToListDict(teamResult)
    teamKey = teamList[0]["teamKey"]

    if isInt(page):
        page = int(page)
    else:
        addUserLog(request, "单接口管理->查看用例->获取数据->页面参数不合法", "FAIL")
        return HttpResponse("<script>alert('请验证页数参数');</script>")
    execSql = "SELECT t.* from tb_admin_user_team_relation t WHERE t.state = 1 "
    checkList = []
    for key in checkArr:
        if checkArr[key] == "":
            continue
        checkList.append("%%%s%%" % checkArr[key])
        execSql += """ and t.%s """ % key
        execSql += """ LIKE %s"""
    execSql += """and t.teamKey = '%s' """ % teamKey
    execSql += """ ORDER BY %s""" % orderBy
    context = pagination(sqlStr=execSql, attrList=checkList, page=page, pageNum=commonWebConfig.userPageNum)
    teamLeaderList = []
    for pageData in context["pageDatas"]:
        pageData["userName"] = TbUser.objects.get(loginName=pageData["loginName"]).userName
        pageData["isTeamLeader"] = len(TbAdminUserRoleRelation.objects.filter(teamKey=teamList[0]["teamKey"],loginName=pageData["loginName"],state=1)) != 0 and True or False
        if pageData["isTeamLeader"]:
            teamLeaderList.append(pageData)
    for pageData in context["pageDatas"]:
        if not pageData["isTeamLeader"]:
            teamLeaderList.append(pageData)
    context["pageDatas"] = teamLeaderList
    response = render(request, "myadmin/userRole/subPages/userRole_sub_page.html", context)
    return response

def setTeamLeader(request):
    loginName = request.POST.get("loginName")
    teamId = request.POST.get("teamId")
    teamResult = TbAdminTeam.objects.filter(id=teamId, state=1)
    teamList = dbModelListToListDict(teamResult)
    userRoleResult = TbAdminUserRoleRelation.objects.filter(loginName=loginName, teamKey=teamList[0]["teamKey"])
    userRoleList = dbModelListToListDict(userRoleResult)
    permissionUserList = ["TeamManage", "UserManage"]
    stateDict = {}


    if len(userRoleList) == 0:
        '''loginName不在组长表中，新增'''
        userRole = TbAdminUserRoleRelation()
        userRole.loginName = loginName
        userRole.roleKey = "teamLeader"
        userRole.teamKey = teamList[0]["teamKey"]
        userRole.state = 1
        stateDict["state"] = 1
        userRole.save()

        '''给组长赋权--小组管理、用户管理'''

        permissionUserRelationList = TbAdminPlatformPermissionUserRelation.objects.filter(loginName=loginName)
        if len(permissionUserRelationList) == 0:
            for permission in permissionUserList:
                permissionUser = TbAdminPlatformPermissionUserRelation()
                permissionUser.permissionKey = permission
                permissionUser.loginName = loginName
                permissionUser.state = 1
                permissionUser.save()
        else:
            userRelation = TbAdminPlatformPermissionUserRelation.objects.filter(loginName=loginName,
                                                                                permissionKey__in=permissionUserList)
            for userRelationIndex in userRelation:
                if userRelationIndex.state == 0:
                    userRelationIndex.state = 1
                    userRelationIndex.save()

        '''给组长赋权--后台的小组管理、用户管理权限'''
        managePermissionsList = ["AdminUser", "AdminTeam"]
        userPermissionList = TbAdminManageUserPermissionRelation.objects.filter(loginName=loginName)
        if len(userPermissionList) == 0:
            for permission in managePermissionsList:
                permissionUser = TbAdminManageUserPermissionRelation()
                permissionUser.permissionKey = permission
                permissionUser.loginName = loginName
                permissionUser.state = 1
                permissionUser.save()
        else:
            userRelation = TbAdminManageUserPermissionRelation.objects.filter(loginName=loginName,
                                                                                permissionKey__in=managePermissionsList)
            for userRelationIndex in userRelation:
                if userRelationIndex.state == 0:
                    userRelationIndex.state = 1
                    userRelationIndex.save()

        '''将组长插入到管理员表中'''
        userResult = dbModelListToListDict(TbUser.objects.filter(loginName=loginName, state=1))[0]
        adminUserResult = dbModelListToListDict(TbAdminUser.objects.filter(loginName=loginName))
        if len(adminUserResult) == 0:
            '''组长不在管理员表中'''
            adminUser = TbAdminUser()
            adminUser.loginName = loginName
            pwdMd5 = hashlib.md5()
            pwdMd5.update("123456".encode("utf-8"))
            password = pwdMd5.hexdigest()
            adminUser.passWord = password
            adminUser.userName = userResult["userName"]
            adminUser.email = userResult["email"]
            adminUser.superManager = 0
            adminUser.state = 1
            adminUser.save()
        else:
            if adminUserResult[0]["state"] == 0:
                '''被删除时不是超级管理员'''
                if adminUserResult[0]["superManager"] == 0:
                    adminUserResult[0]["state"] = 1
                    AdminUserService.updateAdminUser(adminUserResult[0])

                else:
                    '''被删除时，是超级管理员'''
                    adminUserResult[0]["superManager"] = 0
                    adminUserResult[0]["state"] = 1
                    AdminUserService.updateAdminUser(adminUserResult[0])

            else:
                userRelation = TbAdminManageUserPermissionRelation.objects.filter(loginName=loginName,
                                                                                  permissionKey__in=managePermissionsList)
                if len(userRelation) == 0:
                    for permission in managePermissionsList:
                        permissionUser = TbAdminManageUserPermissionRelation()
                        permissionUser.permissionKey = permission
                        permissionUser.loginName = loginName
                        permissionUser.state = 1
                        permissionUser.save()
                else:
                    userRelation.update(state=1)
        return HttpResponse(ApiReturn(body=stateDict).toJson())
    else:
        '''loginName在组长表中'''
        if userRoleList[0]["state"] == 0:
            '''设置组长'''
            userRoleList[0]["state"] = 1
            stateDict["state"] = 1
            UserRoleRelationService.updateUserRole(userRoleList[0])
            platformPermissionUserRelationList = TbAdminPlatformPermissionUserRelation.objects.filter(
                loginName=loginName, permissionKey__in=permissionUserList)
            if len(platformPermissionUserRelationList) == 0:
                for permission in permissionUserList:
                    permissionUser = TbAdminPlatformPermissionUserRelation()
                    permissionUser.permissionKey = permission
                    permissionUser.loginName = loginName
                    permissionUser.state = 1
                    permissionUser.save()
            else:
                platformPermissionUserRelationList.update(state=1)

            '''不管组长在管理员表中state是否为1，都将state置为1'''
            adminUserList = dbModelListToListDict(TbAdminUser.objects.filter(loginName=loginName))
            if adminUserList[0]["state"] == 0:
                adminUserList[0]["state"] = 1
                adminUserList[0]["superManager"] = 0
                AdminUserService.updateAdminUser(adminUserList[0])

            '''给组长赋权--后台的小组管理、用户管理权限'''
            managePermissionsList = ["AdminUser", "AdminTeam"]
            userPermissionList = TbAdminManageUserPermissionRelation.objects.filter(loginName=loginName)
            if len(userPermissionList) == 0:
                for permission in managePermissionsList:
                    permissionUser = TbAdminManageUserPermissionRelation()
                    permissionUser.permissionKey = permission
                    permissionUser.loginName = loginName
                    permissionUser.state = 1
                    permissionUser.save()
            else:
                userRelation = TbAdminManageUserPermissionRelation.objects.filter(loginName=loginName,
                                                                                  permissionKey__in=managePermissionsList)
                for userRelationIndex in userRelation:
                    if userRelationIndex.state == 0:
                        userRelationIndex.state = 1
                        userRelationIndex.save()
            return HttpResponse(ApiReturn(body=stateDict).toJson())


def delTeamLeader(request):
    currentUser = request.session.get("adminLoginName")
    loginName = request.POST.get("loginName")
    teamId = request.POST.get("teamId")
    teamResult = TbAdminTeam.objects.filter(id=teamId, state=1)
    teamList = dbModelListToListDict(teamResult)
    userRoleResult = TbAdminUserRoleRelation.objects.filter(loginName=loginName, teamKey=teamList[0]["teamKey"])
    userRoleList = dbModelListToListDict(userRoleResult)
    stateDict = {}
    permissionUserList = ["TeamManage", "UserManage"]

    if userRoleList[0]["state"] == 1:
        if currentUser == loginName:
            return HttpResponse(
                ApiReturn(code=ApiReturn.CODE_WARNING, message="组长不能撤销自己").toJson())
        else:
            '''撤销组长'''
            userRoleList[0]["state"] = 0
            stateDict["state"] = 0
            UserRoleRelationService.updateUserRole(userRoleList[0])

            userRoleList = dbModelListToListDict(TbAdminUserRoleRelation.objects.filter(loginName=loginName, state=1))

            adminUserResult = dbModelListToListDict(TbAdminUser.objects.filter(loginName=loginName))
            if len(userRoleList) == 0:
                '''loginname不是组长了，而且loginName没有任何授权了，说明也不是其他小组的组长了'''
                TbAdminPlatformPermissionUserRelation.objects.filter(loginName=loginName,
                                                                     permissionKey__in=permissionUserList).update(
                    state=0)
                if len(TbAdminPlatformPermissionUserRelation.objects.filter(loginName=loginName, state=1)) == 0:
                    '''如果是超级管理员，就不做什么了；如果不是超级管理员，就state=0'''
                    if adminUserResult[0]["superManager"] == 0:
                        adminUserResult[0]["state"] = 0
                        AdminUserService.updateAdminUser(adminUserResult[0])
                        TbAdminManageUserPermissionRelation.objects.filter(loginName=loginName).update(state=0)

            return HttpResponse(ApiReturn(body=stateDict).toJson())




