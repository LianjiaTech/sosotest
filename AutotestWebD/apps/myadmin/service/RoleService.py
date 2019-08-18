from all_models.models import TbAdminRole

class RoleService(object):

    @staticmethod
    def updateRole(roleData):
        tbModel = TbAdminRole.objects.filter(id=roleData["id"])
        tbModel.update(**roleData)
