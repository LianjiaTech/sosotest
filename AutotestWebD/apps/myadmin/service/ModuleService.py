from all_models.models import TbModules


class ModuleService(object):

    @staticmethod
    def updateModule(moduleData):
        tbModel = TbModules.objects.filter(id=moduleData["id"])
        tbModel.update(**moduleData)
