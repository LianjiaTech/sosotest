from all_models.models import TbConfigHttp


class ConfigHttpService(object):
    
    @staticmethod
    def updateConfigHttp(configHttpData):
        configService = TbConfigHttp.objects.filter(id=configHttpData["id"])
        configService.update(**configHttpData)