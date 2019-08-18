from all_models.models import TbWebPortalStandardTask

class StandardTaskService(object):

    @staticmethod
    def updatePermission(permissionData):
        tbModel = TbWebPortalStandardTask.objects.filter(id=permissionData["id"])
        tbModel.update(**permissionData)
