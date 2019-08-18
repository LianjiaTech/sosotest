from all_models.models import TbBusinessLine


class BusinessLineService(object):

    @staticmethod
    def updateBusinessLine(businessLineData):
        tbModel = TbBusinessLine.objects.filter(id=businessLineData["id"])
        tbModel.update(**businessLineData)
