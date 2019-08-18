from all_models.models import TbUserPermissionRelation

class UserPermissionRelationService(object):

    @staticmethod
    def updateUserPermission(userPermissionData):
        tbModel = TbUserPermissionRelation.objects.filter(id=userPermissionData["id"])
        tbModel.update(**userPermissionData)
