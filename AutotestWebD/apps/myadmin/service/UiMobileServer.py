from all_models.models import TbUiMobileServer

class UiMobileServer(object):

    @staticmethod
    def updateUiMobileServer(permissionData):
        tbModel = TbUiMobileServer.objects.filter(id=permissionData["id"])
        tbModel.update(**permissionData)
