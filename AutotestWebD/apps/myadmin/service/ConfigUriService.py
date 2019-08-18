from all_models.models import TbConfigUri


class ConfigUriService(object):
    
    @staticmethod
    def updateConfigUri(configUriData):
        configUri = TbConfigUri.objects.filter(uriKey=configUriData["uriKey"])
        configUri.update(**configUriData)