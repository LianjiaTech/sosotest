from all_models.models import TbUser, TbAdminUser, TbAdminPlatformPermissionUserRelation

class PlatformPermissionUserService(object):


    @staticmethod
    def updatePermissionUser(userData):
        tbModel = TbAdminPlatformPermissionUserRelation.objects.filter(id=userData["id"])
        tbModel.update(**userData)
