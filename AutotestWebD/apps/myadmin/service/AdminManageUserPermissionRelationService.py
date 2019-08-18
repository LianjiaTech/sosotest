from all_models.models import TbAdminManageUserPermissionRelation


class AdminManageUserPermissionRelationService(object):

    @staticmethod
    def updateUserPermission(userPermissionData):
        tbModel = TbAdminManageUserPermissionRelation.objects.filter(id=userPermissionData["id"])
        tbModel.update(**userPermissionData)
