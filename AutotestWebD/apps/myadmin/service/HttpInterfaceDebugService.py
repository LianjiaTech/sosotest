from all_models.models import TbHttpInterfaceDebug


class HttpInterfaceDebugService(object):

    @staticmethod
    def updateHttpInterfaceDebug(httpInterfaceDebugData):
        configService = TbHttpInterfaceDebug.objects.filter(id=httpInterfaceDebugData["id"])
        configService.update(**httpInterfaceDebugData)