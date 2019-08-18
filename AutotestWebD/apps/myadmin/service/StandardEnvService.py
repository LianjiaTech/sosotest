from all_models.models import TbWebPortalStandardEnv

class StandardEnvService(object):

    @staticmethod
    def updateStandardEnvService(permissionData):
        tbModel = TbWebPortalStandardEnv.objects.filter(id=permissionData["id"])
        tbModel.update(**permissionData)
