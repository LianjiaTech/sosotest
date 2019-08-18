from all_models.models import TbAdminUserRoleRelation


class UserRoleRelationService(object):

    @staticmethod
    def updateUserRole(userRoleData):
        tbModel = TbAdminUserRoleRelation.objects.filter(id=userRoleData["id"])
        tbModel.update(**userRoleData)
