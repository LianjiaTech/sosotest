
from urllib import parse
from apps.common.config import commonWebConfig
from apps.common.func.WebFunc import *
from all_models.models import *
from all_models_for_mock.models import *
from all_models_for_dubbo.models import *
from apps.myadmin.TeamService import TeamService
from apps.myadmin.service.TeamPermissionRelationService import TeamPermissionRelationService
from apps.myadmin.service.TeamUserRelationService import TeamUserRelationService
from apps.common.model.RedisDBConfig import RedisCache
from apps.common.config.permissionConst import PermissionConst
logger = logging.getLogger("django")

def teamCheckPage(request):
    context = {}

    context["team_check"] = "active"

    return render(request,"myadmin/team/admin_team_check.html",context)

def getTeam(request):
    context = {}
    currentUser = request.session.get("adminLoginName")
    '''当前登录用户是否是超级管理员'''
    adminUserList = dbModelListToListDict(TbAdminUser.objects.filter(loginName=currentUser, superManager=1, state=1))
    teamList = []
    if len(adminUserList) == 0:
        '''currentUser不是超级管理员，判断是否是组长'''
        userRoleList = dbModelListToListDict(TbAdminUserRoleRelation.objects.filter(loginName=currentUser, state=1))

        teamKeyList = []

        if len(userRoleList) != 0:
            '''是组长,拿到currenyUser是组长的小组'''
            for userIndex in userRoleList:
                if userIndex["teamKey"] not in teamKeyList:
                    teamKeyList.append(userIndex["teamKey"])
        for teamKey in teamKeyList:
            teamList.extend(dbModelListToListDict(TbAdminTeam.objects.filter(teamKey=teamKey)))
        teamListSorted = sorted(teamList, key=lambda team: team["id"], reverse=True)
        context["pageDatas"] = sorted(teamListSorted, key=lambda team: team["state"], reverse=True)

    else:
        '''currentUser是超级管理员'''
        teamList.extend(dbModelListToListDict(TbAdminTeam.objects.filter()))
        teamListSorted = sorted(teamList, key=lambda team: team["id"], reverse=True)
        context["pageDatas"] = sorted(teamListSorted, key=lambda team: team["state"], reverse=True)

    response = render(request, "myadmin/team/subPages/team_sub_page.html", context)
    return response


def getTeamForId(request):
    teamId = request.POST.get("teamId")
    try:
        teamData = TbAdminTeam.objects.get(id=teamId)
    except Exception as e:
        message = "小组查询出错 %s" % e
        logger.error(message)
        return HttpResponse(ApiReturn(code=ApiReturn.CODE_WARNING,message=message).toJson())
    return HttpResponse(ApiReturn(body=dbModelToDict(teamData)).toJson())

def addTeam(request):
    teamRequest = json.loads(request.POST.get("teamData"))
    logger.info("addTeam %s" % request.POST.get("teamData"))
    teamKey = teamRequest["teamKey"]
    searchResult = TbAdminTeam.objects.filter(teamKey=teamKey)
    '''如果小组没有添加过，那么就新建'''
    if len(searchResult) == 0:
        result = TbAdminTeam()
        result.teamKey = teamRequest["teamKey"]
        result.teamName = teamRequest["teamName"]
        result.teamDesc = teamRequest["teamDesc"]
        result.save()
        if result:
            logger.info("addTeam 小组创建成功 %s" % result)
        '''新建小组后，给小组授权，默认所有权限'''
        TeamService.addPermissionsToTeam(teamKey)

        return HttpResponse(ApiReturn().toJson())
    else:
        '''如果小组有添加过，但是被删除了，那么更新'''
        searchResultList = dbModelListToListDict(searchResult)
        searchResultDict = searchResultList[0]
        if searchResultDict["state"] == 0:

            searchResultDict["state"] = 1
            searchResultDict["teamName"] = teamRequest["teamName"]
            searchResultDict["teamDesc"] = teamRequest["teamDesc"]
            TeamService.updateTeam(searchResultDict)
            '''小组置为有效后，给小组授权，默认所有权限'''
            TeamService.addPermissionsToTeam(teamKey)

            return HttpResponse(ApiReturn().toJson())
        else:
            logger.info("addTeam 小组创建失败")
            return HttpResponse(
                ApiReturn(code=ApiReturn.CODE_WARNING, message="小组创建失败,请检查小组key是否重复").toJson())


def editTeam(request):
    try:
        requestDict =json.loads(request.POST.get("teamData"))
        requestDict["modTime"] = datetime.datetime.now()
        TeamService.updateTeam(requestDict)
    except Exception as e:
        print(traceback.format_exc())
        message = "编辑小组数据发生异常 %s" % e
        logger.info(message)
        return HttpResponse(ApiReturn(code=ApiReturn.CODE_WARNING, message=message).toJson())

    return HttpResponse(ApiReturn().toJson())

def delTeam(request):
    teamId = request.POST.get("teamId", "")
    if not teamId:
        return HttpResponse(ApiReturn(ApiReturn.CODE_WARNING, message="teamId参数错误").toJson())
    try:
        teamData = TbAdminTeam.objects.get(state=1, id=teamId)
    except Exception as e:
        return HttpResponse(ApiReturn(ApiReturn.CODE_WARNING, message="teamId查询错误 %s" % e).toJson())
    teamData.state = 0
    teamData.save()
    '''删除小组后，删除关联关系'''
    TbAdminUserTeamRelation.objects.filter(teamKey=teamData.teamKey, state=1).update(state=0)
    TbAdminTeamPermissionRelation.objects.filter(teamKey=teamData.teamKey, state=1).update(state=0)
    '''删除小组后，要删除小组组长'''
    teamUserRoleList = TbAdminUserRoleRelation.objects.filter(teamKey=teamData.teamKey, state=1)
    '''将小组teamKey的组长删除，并且将组长的授权删除'''
    for teamUserRole in teamUserRoleList:
        teamUserRole.state = 0
        teamUserRole.save()
        relationList = TbAdminPlatformPermissionUserRelation.objects.filter(loginName=teamUserRole.loginName)
        for index in relationList:
            index.state=0
            index.save()
    '''判断该teamKey小组的组长是否为其他小组的组长，如果不是其他小组的组长，就将该loginName从adminUser表中删除'''
    for userIndex in teamUserRoleList:
        if len(TbAdminUserRoleRelation.objects.filter(loginName=userIndex.loginName, state=1)) == 0:
            TbAdminUser.objects.filter(loginName=userIndex.loginName, state=1).update(state=0)

    return HttpResponse(ApiReturn().toJson())

def resetTeam(request):
    teamId = request.POST.get("teamId", "")
    if not teamId:
        return HttpResponse(ApiReturn(ApiReturn.CODE_WARNING, message="teamId参数错误").toJson())
    try:
        teamData = TbAdminTeam.objects.get(state=0, id=teamId)
    except Exception as e:
        return HttpResponse(ApiReturn(ApiReturn.CODE_WARNING, message="teamId查询错误 %s" % e).toJson())
    teamData.state = 1
    teamData.save()
    '''启用小组后， 对小组授权 '''
    TeamService.addPermissionsToTeam(teamData.teamKey)
    return HttpResponse(ApiReturn().toJson())


def addUsersToTeam(request):
    teamRequest = json.loads(request.POST.get("teamUsersData"))
    logger.info("addTeam %s" % request.POST.get("teamUsersData"))
    teamId = teamRequest["teamId"]

    teamKey = TbAdminTeam.objects.get(id=teamId).teamKey
    loginNames = teamRequest["loginNames"]
    userTeamData = {}

    relationData = TbAdminUserTeamRelation.objects.filter(teamKey=teamKey)
    for relation in relationData:

        relationLoginName = relation.loginName
        '''如果数据库中已经存在要添加的loginName'''
        if relationLoginName in loginNames:
            userTeamData["teamKey"] = teamKey
            userTeamData["loginName"] = relationLoginName
            '''判断该loginName用户是否已经被删除'''
            if relation.state == 0:
                relation.state = 1
                TeamUserRelationService.updateTeamUser(dbModelToDict(relation))
        else:
            '''如果数据库中的loginName没有要添加的loginName中，说明该用户要被删除'''
            if relation.state == 1:
                userTeamData["teamKey"] = teamKey
                userTeamData["loginName"] = relationLoginName
                relation.state = 0
                TeamUserRelationService.updateTeamUser(dbModelToDict(relation))

    for loginName in loginNames:
        userTeamData["teamKey"] = teamKey
        userTeamData["loginName"] = loginName
        '''判断小组中是否已经存在要添加的loginName'''
        data = TbAdminUserTeamRelation.objects.filter(loginName=loginName, teamKey=teamKey)
        '''要添加的loginName没有在小组中，新加loginName到数据库中'''
        if len(data) == 0:
            result = TbAdminUserTeamRelation()
            result.teamKey = userTeamData["teamKey"]
            result.loginName = userTeamData["loginName"]
            userResult = TbUser.objects.filter(loginName=loginName, state=1)
            userList = dbModelListToListDict(userResult)
            result.userName = userList[0]["userName"]
            result.save()
        else:
            '''要添加的loginName在小组中'''
            for user in data:
                if user.state == 0:
                    TeamUserRelationService.updateTeamUser(userTeamData)
    return HttpResponse(ApiReturn().toJson())



def getAllUsers(request):
    try:
        usersResult = TbUser.objects.filter(state=1)
        usersDict = dbModelListToListDict(usersResult)
    except Exception as e:
        message = "查询用户出错 %s" % e
        logger.error(message)
        return HttpResponse(ApiReturn(code=ApiReturn.CODE_WARNING, message=message).toJson())
    return HttpResponse(ApiReturn(body=usersDict).toJson())


def getAllSelectedUsers(request):
    teamId = request.POST.get("teamId")
    teamResult = TbAdminTeam.objects.filter(id=teamId, state=1)
    teamList = dbModelListToListDict(teamResult)
    teamDict = teamList[0]
    teamKey = teamDict["teamKey"]
    usersResult = TbAdminUserTeamRelation.objects.filter(state=1, teamKey=teamKey)
    if len(usersResult) == 0:
        return HttpResponse(ApiReturn().toJson())
    else:
        usersList = dbModelListToListDict(usersResult)
        list = []
        for user in usersList:
            usersDict = user
            loginName = usersDict["loginName"]
            users = TbUser.objects.filter(loginName=loginName)
            usersListNew = dbModelListToListDict(users)
            if len(usersListNew) == 0:
                list = []
            else:
                list.append(usersListNew[0])
        return HttpResponse(ApiReturn(body=list).toJson())

def deleteSelectedUsers(request):
    teamId = request.POST.get("teamId")
    teamResult = TbAdminTeam.objects.filter(id=teamId, state=1)
    teamList = dbModelListToListDict(teamResult)
    teamDict = teamList[0]
    teamKey = teamDict["teamKey"]
    usersResult = TbAdminUserTeamRelation.objects.filter(state=1, teamKey=teamKey)
    if len(usersResult) == 0:
        return HttpResponse(ApiReturn().toJson())
    else:
        usersList = dbModelListToListDict(usersResult)
        list = []
        for user in usersList:
            usersDict = user
            loginName = usersDict["loginName"]
            users = TbUser.objects.filter(loginName=loginName)
            usersListNew = dbModelListToListDict(users)
            if len(usersListNew) != 0 :
                list.append(usersListNew[0])
        return HttpResponse(ApiReturn(body=list).toJson())

def addPermissionsToTeam(request):
    teamRequest = json.loads(request.POST.get("teamPermissionsData"))
    logger.info("teamPermission %s" % request.POST.get("teamPermissionsData"))
    # teamId = teamRequest["teamId"]
    # teamData = TbAdminTeam.objects.filter(id=teamId)
    # teamList = dbModelListToListDict(teamData)
    # teamDict = teamList[0]
    teamKey = teamRequest["teamKey"]
    permissionKeys = teamRequest["permissionKeys"]
    teamPermissionsData = {}

    relationData = TbAdminTeamPermissionRelation.objects.filter(teamKey=teamKey)
    relationDataList = dbModelListToListDict(relationData)

    for relation in relationDataList:
        relationPermissionKey = relation["permissionKey"]
        '''如果小组已经授权过permissionKey,并且permissionKey在这次要授权的列表中，说明这次是要给小组授权permissionKey'''
        if relationPermissionKey in permissionKeys:
            if relation["state"] == 0:
                relation["state"] =1
                TeamPermissionRelationService.updateTeamPermission(relation)
        else:
            '''如果小组已经授权过permissionKey，但是permissionKey不在这次要授权的列表中，说明这次不给小组授权permissionKey，要将原有permissionKey的授权删除'''
            if relation["state"] == 1:
                relation["state"] = 0
                TeamPermissionRelationService.updateTeamPermission(relation)
    '''判断该小组是否已经有这次要授的权限关联关系，如果没有，那么就新建授权关系；如果有，那么判断是都否是有效的，如果无效，需要更新'''
    for permissionKey in permissionKeys:
        teamPermissionsData["teamKey"] = teamKey
        teamPermissionsData["permissionKey"] = permissionKey
        data = TbAdminTeamPermissionRelation.objects.filter(teamKey=teamKey, permissionKey=permissionKey)
        if len(data) == 0:
            result = TbAdminTeamPermissionRelation()
            result.teamKey = teamPermissionsData["teamKey"]
            result.permissionKey = teamPermissionsData["permissionKey"]
            result.save()
        else:
            permission = dbModelListToListDict(data)
            for user in permission:
                if user["state"] == 0:
                    TeamPermissionRelationService.updateTeamPermission(teamPermissionsData)
    return HttpResponse(ApiReturn().toJson())

def getTeammates(request):
    teamId = request.POST.get("teamId")
    teamKey = dbModelListToListDict(TbAdminTeam.objects.filter(id=teamId, state=1))[0]["teamKey"]
    teammatesList = TbAdminUserTeamRelation.objects.filter(teamKey=teamKey, state=1)
    loginNamesDict = {}
    if len(teammatesList) == 0:
        return HttpResponse(ApiReturn(code=ApiReturn.CODE_ERROR, message="小组没有成员").toJson())
    for teamMatesIndex in teammatesList:
        try:
            userName = TbUser.objects.get(loginName=teamMatesIndex.loginName, state=1).userName
            loginNamesDict[teamMatesIndex.loginName] = userName
        except:
            continue
    return HttpResponse(ApiReturn(body=loginNamesDict).toJson())

def tansferData(request):
    dataType = json.loads(request.POST.get("dataDict"))
    dataTypeList = dataType["dataTypeList"]
    fromUsersList = dataType["fromUsersList"]
    toUser = dataType["toUser"]
    modTime = datetime.datetime.now()
    for typeIndex in dataTypeList:
        for user in fromUsersList:
            if typeIndex == "interface":
                TbHttpInterface.objects.filter(addBy=user).update(addBy=toUser, modTime=modTime)
            elif typeIndex == "testcase":
                TbHttpTestcase.objects.filter(addBy=user).update(addBy=toUser, modTime=modTime)
            elif typeIndex == "task":
                TbTask.objects.filter(addBy=user).update(addBy=toUser, modTime=modTime)
            elif typeIndex == "taskSuite":
                TbTaskSuite.objects.filter(addBy=user).update(addBy=toUser, modTime=modTime)
            if typeIndex == "dubbo_interface":
                Tb2DubboInterface.objects.filter(addBy=user).update(addBy=toUser, modTime=modTime)
            elif typeIndex == "dubbo_testcase":
                Tb2DubboTestcase.objects.filter(addBy=user).update(addBy=toUser, modTime=modTime)
            elif typeIndex == "dubbo_task":
                Tb2DubboTask.objects.filter(addBy=user).update(addBy=toUser, modTime=modTime)
            elif typeIndex == "dubbo_taskSuite":
                TbTaskSuite.objects.filter(addBy=user).update(addBy=toUser, modTime=modTime)
            elif typeIndex == "globalVars":
                TbGlobalVars.objects.filter(addBy=user).update(addBy=toUser, modTime=modTime)
            elif typeIndex == "globalText":
                TbGlobalText.objects.filter(addBy=user).update(addBy=toUser, modTime=modTime)
            elif typeIndex == "configService":
                TbConfigUri.objects.filter(addBy=user).update(addBy=toUser, modTime=modTime)
            elif typeIndex == "configHttp":
                TbConfigHttp.objects.filter(addBy=user).update(addBy=toUser, modTime=modTime)
            elif typeIndex == "envUriConf":
                TbEnvUriConf.objects.filter(addBy=user).update(addBy=toUser, modTime=modTime)
            elif typeIndex == "dataKeyWord":
                Tb4DataKeyword.objects.filter(addBy=user,type="DATA_KEYWORD").update(addBy=toUser, modTime=modTime)
            elif typeIndex == "dataPythonCode":
                Tb4DataKeyword.objects.filter(addBy=user,type="PYTHON_CODE").update(addBy=toUser, modTime=modTime)
            elif typeIndex == "dataMock":
                Tb4MockHttp.objects.filter(addBy=user).update(addBy=toUser, modTime=modTime)


    return HttpResponse(ApiReturn().toJson())


def getTeamPermission(request):

    teamKey = request.POST.get("teamKey")

    allUrl = TbAdminInterfacePermissionRelation.objects.filter(state=1)
    for urlIndex in allUrl:
        try:
            #先删缓存
            RedisCache().del_data("%s_%s_%s" % (PermissionConst.team_url_permission,teamKey,urlIndex.url))
        except :
            pass
    teamPermission = TbAdminTeamPermissionRelation.objects.filter(teamKey=teamKey,state=1)
    teamPermissionList = []
    for index in teamPermission:
        tmpDict = {}
        tmpDict["permissionKey"] = index.permissionKey
        try:
            tmpDict["permissionName"] = TbAdminInterfacePermissionRelation.objects.get(permissionKey=index.permissionKey).permissionName
        except:
            tmpDict["permissionName"] = ""
        teamPermissionList.append(tmpDict)
    return HttpResponse(ApiReturn(body=teamPermissionList).toJson())

def permissionReload(request):
    interfaceData = TbAdminInterfacePermissionRelation.objects.all()
    for index in interfaceData:
        try:
            RedisCache().del_data("%s_%s" % (PermissionConst.urlDefaultPermission,index.url))
            RedisCache().del_data("%s_%s" % (PermissionConst.urlAllPermission,index.url))
        except:
            pass

        teamData = TbAdminTeam.objects.all()
        for teamIndex in teamData:
            try:
                RedisCache().del_data("%s_%s_%s" % (PermissionConst.team_url_permission,teamIndex.teamName,index.url))
                print("%s_%s_%s" % (PermissionConst.team_url_permission,teamIndex.teamName,index.url))
            except:
                pass


    userData = TbUser.objects.all()
    for userIndex in userData:
        try:
            RedisCache().del_data("%s_%s" % (PermissionConst.user_permission, userIndex.loginName))
        except:
            pass

    return HttpResponse(ApiReturn().toJson())