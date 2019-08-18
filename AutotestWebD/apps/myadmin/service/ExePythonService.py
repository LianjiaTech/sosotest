from all_models.models import TbExecPythonAttrs


class ExePythonService(object):

    @staticmethod
    def updateModule(moduleData):
        tbModel = TbExecPythonAttrs.objects.filter(id=moduleData["id"])
        tbModel.update(**moduleData)
