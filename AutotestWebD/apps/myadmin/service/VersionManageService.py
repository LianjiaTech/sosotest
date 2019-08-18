from all_models.models import TbVersion

class VersionManageService(object):

    @staticmethod
    def updateVersionManage(permissionData):
        tbModel = TbVersion.objects.filter(id=permissionData["id"])
        tbModel.update(**permissionData)
