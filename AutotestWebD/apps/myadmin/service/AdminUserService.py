from all_models.models import *
from apps.common.func.CommonFunc import dbModelListToListDict

class AdminUserService(object):

    @staticmethod
    def getUsers():
        return TbUser.objects.all()

    @staticmethod
    def getUserByLoginname(loginname):
        return TbUser.objects.filter(loginname=loginname)

    @staticmethod
    def updateAdminUser(userData):
        tbModel = TbAdminUser.objects.filter(id=userData["id"])
        tbModel.update(**userData)


    @staticmethod
    def addDefaultPermission(loginName):
        permissionResult = TbAdminManagePermission.objects.filter(state=1, isDefaultPermission=1)
        permissionResultList = dbModelListToListDict(permissionResult)

        '''如果loginName没有授权历史，那么就在数据库中插入数据'''
        for permission in permissionResultList:
            permissionRelation = TbAdminManageUserPermissionRelation.objects.filter(loginName=loginName, permissionKey=permission["permissionKey"])

            if len(permissionRelation) == 0:
                permissionKey = permission["permissionKey"]
                relationResult = TbAdminManageUserPermissionRelation()
                relationResult.permissionKey = permissionKey
                relationResult.loginName = loginName
                relationResult.state = 1
                relationResult.save()
            else:
                '''如果loginName有授权历史，并且已经被删除，那么进行更新操作'''
                for permissionIndex in permissionRelation:
                    if permissionIndex.state == 0:
                        permissionIndex.state = 1
                        permissionIndex.save()



    @staticmethod
    def addAllPermissions(loginName):
        permissionResult = TbAdminManagePermission.objects.filter(state=1)
        permissionResultList = dbModelListToListDict(permissionResult)
        '''如果loginName没有授权历史，那么就在数据库中插入数据'''
        for permission in permissionResultList:
            permissionRelation = TbAdminManageUserPermissionRelation.objects.filter(loginName=loginName, permissionKey=permission["permissionKey"])

            if len(permissionRelation) == 0:
                permissionKey = permission["permissionKey"]
                relationResult = TbAdminManageUserPermissionRelation()
                relationResult.permissionKey = permissionKey
                relationResult.loginName = loginName
                relationResult.state = 1
                relationResult.save()
            else:
                '''如果loginName有授权历史，并且已经被删除，那么进行更新操作'''
                for permissionIndex in permissionRelation:
                    if permissionIndex.state == 0:
                        permissionIndex.state = 1
                        permissionIndex.save()