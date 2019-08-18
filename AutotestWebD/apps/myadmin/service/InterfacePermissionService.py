from all_models.models import TbAdminInterfacePermissionRelation


class InterfacePermissionService(object):

    @staticmethod
    def updateInterfacePermission(interfacePermissionData):
        tbModel = TbAdminInterfacePermissionRelation.objects.filter(id=interfacePermissionData["id"])
        tbModel.update(**interfacePermissionData)
