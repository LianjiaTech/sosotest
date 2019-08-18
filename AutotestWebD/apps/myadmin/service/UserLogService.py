from all_models.models import TbUserLog

class UserLogService(object):

    @staticmethod
    def updateUserLogService(permissionData):
        tbModel = TbUserLog.objects.filter(id=permissionData["id"])
        tbModel.update(**permissionData)
