from all_models.models import TbSource


class SourceService(object):

    @staticmethod
    def updateSource(sourceData):
        tbModel = TbSource.objects.filter(id=sourceData["id"])
        tbModel.update(**sourceData)
