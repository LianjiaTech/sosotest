from all_models.models import TbConfigService


class ConfigService(object):
    
    @staticmethod
    def updateConfigService(configServiceData):
        configService = TbConfigService.objects.filter(id=configServiceData["id"])
        configService.update(**configServiceData)