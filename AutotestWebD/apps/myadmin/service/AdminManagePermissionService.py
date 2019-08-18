from all_models.models import TbAdminManagePermission

class AdminManagePermissionService(object):

    @staticmethod
    def updatePermission(permissionData):
        tbModel = TbAdminManagePermission.objects.filter(id=permissionData["id"])
        tbModel.update(**permissionData)
