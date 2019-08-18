from apps.common.model.RedisDBConfig import RedisCache
from all_models.models import TbAdminUser,TbAdminInterfacePermissionRelation,TbUser,TbAdminUserTeamRelation,TbAdminTeamPermissionRelation,TbUserPermissionRelation
from apps.common.config.permissionConst import PermissionConst
import json

class UserPermissionService(object):

    @staticmethod
    def get_user_url_all_permission(loginName,url):
        userPermissionList = []
        tb_url_permission_key = TbAdminInterfacePermissionRelation.objects.filter(url=url)
        for index in tb_url_permission_key:
            tb_user_permission = TbUserPermissionRelation.objects.filter(loginName=loginName,
                                                                              permissionKey=index.permissionKey)
            for user_permissionIndex in tb_user_permission:
                if user_permissionIndex.permissionKey not in userPermissionList:
                    userPermissionList.append(user_permissionIndex.permissionKey)
        return userPermissionList
    @staticmethod
    def get_user_default_permission(loginName):
        try:
            userPermission = json.loads(RedisCache().get_data("%s_%s" % (PermissionConst.user_permission, loginName)))
            return True, userPermission
        except:
            # 从redis拿不到 从数据拿  然后将信息写入redis
            try:
                userDefaultPermission = int(TbUser.objects.get(state=1, loginName=loginName).defaultPermission)
                userPermission = {}
                userPermission["defaultPermission"] = userDefaultPermission
                if len(TbUserPermissionRelation.objects.filter(state=1, loginName=loginName)) > 0:
                    userPermission["otherPermission"] = 1
                else:
                    userPermission["otherPermission"] = 0
                RedisCache().set_data("%s_%s" % (PermissionConst.user_permission, loginName),
                                      json.dumps(userPermission),
                                      60 * 60 * 24 * 15)
                return True, userPermission
            except:
                return False, {}

    @staticmethod
    def get_url_default_permissions(url):
        #先去缓存拿
        try:
            urlDefaultPermission = json.loads(RedisCache().get_data("%s_%s" % (PermissionConst.urlDefaultPermission,url)))
        except:
            #缓存没拿到 去数据库拿再写入缓存
            modList = TbAdminInterfacePermissionRelation.objects.filter(url=url,isDefault=1,state=1)
            urlDefaultPermission = []
            for index in modList:
                urlDefaultPermission.append(index.permission)

            RedisCache().set_data("%s_%s" % (PermissionConst.urlDefaultPermission,url),json.dumps(urlDefaultPermission))
        return urlDefaultPermission

    @staticmethod
    def get_url_all_permissions(url):
        # 先去缓存拿
        try:
            urlAllPermission = json.loads(RedisCache().get_data("urlAllPermission_%s" % url))
        except:
            # 缓存没拿到 去数据库拿再写入缓存
            modList = TbAdminInterfacePermissionRelation.objects.filter(url=url,state=1)
            urlAllPermission = []
            for index in modList:
                urlAllPermission.append(index.permission)

            RedisCache().set_data("%s_%s" % (PermissionConst.urlAllPermission,url), json.dumps(urlAllPermission))
        return urlAllPermission

    #获取用户自己的权限
    @staticmethod
    def get_user_url_permissions(url,loginName,otherLoginNameList):
        userPermissionDict = {"permissions":{},"isSuccess":True}

        for otherLoginName in otherLoginNameList:
            userPermissionDict["permissions"][otherLoginName] = []
            otherLoginNamePermission = userPermissionDict["permissions"][otherLoginName]

            #如果用户是超级管理员 则有所有权限
            if len(TbAdminUser.objects.filter(loginName=loginName, state=1, superManager=1)) > 0:
                tmpPermissions = TbAdminInterfacePermissionRelation.objects.filter(url=url,state=1)
                for index in tmpPermissions:
                    otherLoginNamePermission.append(index.permission)
                continue


            if otherLoginName == loginName or otherLoginName == "None" or otherLoginName == "" or otherLoginName == None:
                tmpPermissions = TbAdminInterfacePermissionRelation.objects.filter(url=url, state=1)
                for index in tmpPermissions:
                    otherLoginNamePermission.append(index.permission)
                continue

            userPermissionResult,userPermission = UserPermissionService.get_user_default_permission(loginName)
            if userPermissionResult:
                userDefaultPermission = int(userPermission["defaultPermission"])
                userOtherPermission = int(userPermission["otherPermission"])
            else:
                userPermissionDict["permissions"][otherLoginName] = []
                continue

            if userDefaultPermission == 1:
                tmpDefaultPermission = UserPermissionService.get_url_default_permissions(url)
                for index in tmpDefaultPermission:
                    if index not in otherLoginNamePermission:
                        otherLoginNamePermission.append(index)

            #查询用户是否有其他权限
            if userOtherPermission == 1:
                allPermission = TbAdminInterfacePermissionRelation.objects.filter(state=1,url=url)
                for index in allPermission:
                    if len(TbUserPermissionRelation.objects.filter(state=1,loginName=loginName,permissionKey=index.permissionKey)) > 0:
                        otherLoginNamePermission.append(index.permission)

            #查我和此人同在哪些小组
            loginNameTeamList = TbAdminUserTeamRelation.objects.filter(loginName=loginName,state=1)
            for teamIndex in loginNameTeamList:
                togetherTeam = TbAdminUserTeamRelation.objects.filter(loginName=otherLoginName,teamKey=teamIndex.teamKey,state=1)
                for togetherTeamIndex in togetherTeam:
                    try:
                        tmpTeamPermission = json.loads(RedisCache().get_data("%s_%s_%s" % (PermissionConst.team_url_permission,togetherTeamIndex.teamKey, url)))
                        for tmpIndex in tmpTeamPermission:
                            if tmpIndex not in otherLoginNamePermission:
                                otherLoginNamePermission.append(tmpIndex)
                    except:
                        tmpTeamPermission = []
                        tmpTeamPermissionList = TbAdminTeamPermissionRelation.objects.filter(state=1,teamKey=togetherTeamIndex.teamKey)
                        for tmpIndex in tmpTeamPermissionList:
                            tmpPermission = TbAdminInterfacePermissionRelation.objects.filter(state=1,url=url,permissionKey=tmpIndex.permissionKey)
                            for tmpPermissionIndex in tmpPermission:
                                if tmpPermissionIndex.permission not in otherLoginNamePermission:
                                    otherLoginNamePermission.append(tmpPermissionIndex.permission)

                                if tmpPermissionIndex.permission not in tmpTeamPermission:
                                    tmpTeamPermission.append(tmpPermissionIndex.permission)
                        RedisCache().set_data("%s_%s_%s" % (PermissionConst.team_url_permission,togetherTeamIndex.teamKey, url),json.dumps(tmpTeamPermission))
        return userPermissionDict




if __name__ == "__main__":
    print(1)
     # print(UserService.getUsers()[0])
    #permissionDict = UserPermission.getUserPermissions("liyc", "/interfaceTest/HTTP_InterfaceListCheck")
    #print(permissionDict)
    # print("permissionDict:", permissionDict)
    #print("interfaceDict:", interfaceDict)
     # permissionsList = UserPermission.getOthersPermissions("zhouxj", ["zhouxj"], "/interfaceTest/HTTP_InterfaceDel")
     # print("permissionsList:", permissionsList)
  #  print(UserService.getUserByLoginname(UserService.getUsers()[0].loginName))
