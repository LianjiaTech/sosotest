from all_models.models import TbWebPortalBusinessLine


class WebportalBusinessLineService(object):

    @staticmethod
    def updateBusinessLine(businessLineData):
        tbModel = TbWebPortalBusinessLine.objects.filter(id=businessLineData["id"])
        tbModel.update(**businessLineData)
