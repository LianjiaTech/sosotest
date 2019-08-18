from apps.common.func.WebFunc import *
from apps.common.model.RedisDBConfig import RedisCache
from apps.common.config.permissionConst import PermissionConst

class TeamService(object):

    @staticmethod
    def updateTeam(teamData):
        tbModel = TbAdminTeam.objects.filter(id=teamData["id"])
        tbModel.update(**teamData)

    @staticmethod
    def deleteTeamLeader(teamData):
        teamLeaderList = TbAdminUserRoleRelation.objects.filter(teamKey=teamData.teamKey, state=1)
        if len(teamLeaderList) != 0:
            teamLeaderList.update(state=0)
            for teamLeader in teamLeaderList:
                userRole = TbAdminUserRoleRelation.objects.filter(loginName=teamLeader.loginName, state=1)
                if len(userRole) == 0:
                    TbAdminUser.objects.filter(loginName=userRole.loginName, state=1).update(state=0)

    @staticmethod
    def addPermissionsToTeam(teamKey):

        #清空有关本小组的缓存
        allUrlData = TbAdminInterfacePermissionRelation.objects.filter(state=1)
        for index in allUrlData:
            try:
                RedisCache().del_data("team_url_%s_%s" % (teamKey,index.url))
            except:
                continue

        permissionResult = TbAdminInterfacePermissionRelation.objects.filter(state=1)
        permissionResultList = dbModelListToListDict(permissionResult)
        for permission in permissionResultList:
            teamPermissionList = TbAdminTeamPermissionRelation.objects.filter(teamKey=teamKey,permissionKey=permission["permissionKey"])
            if len(teamPermissionList) == 0:
                permissionKey = permission["permissionKey"]
                relationResult = TbAdminTeamPermissionRelation()
                relationResult.permissionKey = permissionKey
                relationResult.teamKey = teamKey
                relationResult.state = 1
                relationResult.save()
            else:
                for permissionIndex in teamPermissionList:
                    if permissionIndex.state == 0:
                        permissionIndex.state = 1
                        permissionIndex.save()